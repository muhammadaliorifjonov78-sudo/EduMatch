from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import random
import os

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

from .models import Cars, MatchingGroup, Course, TelegramContact, VerificationCode
from .serializers import (
    CarsSerializer,
    MatchingGroupSerializer,
    CourseSerializer,
    RegisterSerializer,
    LoginSerializer,
    VerifyCodeSerializer,
)
from .permissions import IsManager


class cars_list(ListCreateAPIView):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer


class MatchingGroupFilterView(APIView):
    def get(self, request):
        queryset = MatchingGroup.objects.all()

        direction = request.query_params.get("direction")
        location = request.query_params.get("location")
        time = request.query_params.get("time")
        days = request.query_params.getlist("days")

        if direction:
            queryset = queryset.filter(direction__iexact=direction)
        if location:
            queryset = queryset.filter(location__iexact=location)
        if time:
            queryset = queryset.filter(time__iexact=time)

        groups = []
        for group in queryset:
            if days and not all(day in group.days for day in days):
                continue
            groups.append(group)

        return Response(MatchingGroupSerializer(groups, many=True, context={"request": request}).data)


class CourseFilterView(ListCreateAPIView):
    """
    GET  /api/courses/
    GET  /api/courses/?category=Dasturlash
    GET  /api/courses/?category=Web%20Dasturlash
    GET  /api/courses/?category=Dasturlash&search=python

    POST /api/courses/ -> faqat Manager/staff/superuser.

    category berilmasa barcha kurslar qaytadi.
    """
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        queryset = Course.objects.all()

        category = self.request.query_params.get("category", "").strip()
        search = self.request.query_params.get("search", "").strip()

        if category:
            queryset = queryset.filter(category__iexact=category)

        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                teacher__icontains=search
            ) | queryset.filter(
                category__icontains=search
            )

        return queryset.distinct()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return [AllowAny()]


class CourseDetailView(APIView):
    """
    Kursni bitta ID bo'yicha ko'rish.
    """
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Kurs topilmadi."}, status=404)

        return Response(
            CourseSerializer(course, context={"request": request}).data
        )





def send_telegram_code(phone_number, code):
    try:
        from bot import send_code_to_phone
        return send_code_to_phone(phone_number, code)
    except Exception as exc:
        print("Telegram error:", exc)
        return False


def create_and_send_code(user, phone_number):
    contact = TelegramContact.objects.filter(phone_number=phone_number).first()
    if not contact:
        return False, "Bu telefon raqami Telegram botga ulanmagan. Telegram'da EduMatch botiga /start yuboring va telefon raqamingizni ulashing."

    code = str(random.randint(1000, 9999))
    verification, _ = VerificationCode.objects.get_or_create(user=user)
    verification.code = code
    verification.phone_number = phone_number
    verification.telegram_username = contact.telegram_username
    verification.is_verified = False
    verification.created_at = timezone.now()
    verification.save()

    sent = send_telegram_code(phone_number, code)
    if not sent:
        return False, "Telegramga kod yuborilmadi. Bot ishlayotganini tekshiring."
    return True, "Tasdiqlash kodi Telegramga yuborildi."


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        if User.objects.filter(username=phone_number).exists():
            return Response({"success": False, "message": "Bu telefon raqami allaqachon ro'yxatdan o'tgan. Login qiling."}, status=status.HTTP_400_BAD_REQUEST)

        if not TelegramContact.objects.filter(phone_number=phone_number).exists():
            return Response({"success": False, "message": "Avval Telegram'da EduMatch botiga /start yuboring va telefon raqamingizni ulashing."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=phone_number, password=password)
        sent, message = create_and_send_code(user, phone_number)
        if not sent:
            user.delete()
            return Response({"success": False, "message": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, "message": message, "phone_number": phone_number}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        user = authenticate(username=phone_number, password=password)
        if user is None:
            return Response({"success": False, "message": "Telefon raqami yoki parol noto'g'ri."}, status=status.HTTP_401_UNAUTHORIZED)

        sent, message = create_and_send_code(user, phone_number)
        if not sent:
            return Response({"success": False, "message": message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": True, "message": message, "phone_number": phone_number})


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(username=phone_number)
            verification = user.verification
        except (User.DoesNotExist, VerificationCode.DoesNotExist):
            return Response({"success": False, "message": "Tasdiqlash kodi topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        if verification.is_expired():
            verification.is_verified = False
            verification.save(update_fields=["is_verified"])
            return Response({"success": False, "message": "Kodning muddati tugagan. Qayta login qiling."}, status=status.HTTP_400_BAD_REQUEST)

        if verification.code != code:
            return Response({"success": False, "message": "Kod noto'g'ri. Home page'ga kirishga ruxsat berilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        verification.is_verified = True
        verification.save(update_fields=["is_verified"])
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"success": True, "message": "Kod to'g'ri. Xush kelibsiz!", "token": token.key, "phone_number": phone_number, "redirect": "/home"})

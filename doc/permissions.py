from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Kurs yaratish faqat Manager guruhidagi user yoki staff/superuser uchun.
    GET endpoint esa alohida view orqali ochiq qoladi.
    """
    message = "Kurs qo'shish uchun Manager huquqi kerak."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.is_superuser
            or user.is_staff
            or user.groups.filter(name="Manager").exists()
        )

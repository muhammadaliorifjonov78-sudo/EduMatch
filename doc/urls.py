from django.urls import path

from .views import (
    cars_list,
    CourseDetailView,
    CourseFilterView,
    LoginView,
    MatchingGroupFilterView,
    RegisterView,
    VerifyCodeView,
)

urlpatterns = [
    path("api/cars/", cars_list.as_view()),
    path("api/groups/filter/", MatchingGroupFilterView.as_view()),
    path("api/courses/", CourseFilterView.as_view()),
    path("api/courses/<int:pk>/", CourseDetailView.as_view()),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify-code"),
]

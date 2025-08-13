from django.urls import path
from .views import AcceptAppplicationView, CreateJobView, GetDashboardDetails, Home, ProductView, order_item, GetUserInformationView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("", Home, name="Home response"), 
    # path("create/user/", CreateUserView.as_view(), name="Register User"), 
    path("product/", ProductView.as_view(), name="Get/Create Products"),
    path("order/", order_item.as_view(), name="Get/Create Orders"),

    # new endpoints
    path("create-list-job/", CreateJobView.as_view(), name="Get/Create Jobs"),
    path("profile/", GetUserInformationView.as_view(), name="Get/Create Jobs"),
    path("get-dash/", GetDashboardDetails.as_view()),
    path("apply-status/", AcceptAppplicationView.as_view()),
    path("cron/", Home, name = "Start up cron")
]
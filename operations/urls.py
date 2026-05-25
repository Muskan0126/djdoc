from django.urls import path
from . import views 


# Create your views here.
app_name = "operations"
urlpatterns  = [path("", views.index, name = 'index'),
				path("signup/", views.signup, name = 'signup'),
				path("login/", views.user_login, name = 'login'),
                path("logout/", views.user_logout, name="logout"),
				]
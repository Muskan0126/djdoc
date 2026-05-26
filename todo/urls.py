from . import views
from django.urls import path
from .views import TaskDetailView,TaskListCreateView,login_page,signup_page,home_page

app_name = "todo"
urlpatterns  = [path("", TaskListCreateView.as_view()),
				path("<int:pk>/", TaskDetailView.as_view()),
                path("login/",login_page),
                path('signup/',signup_page),
                path('home/',home_page),
				]
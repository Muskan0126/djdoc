from . import views
from django.urls import path
from .views import TaskDetailView,TaskListCreateView,SignupView,LoginView

app_name = "todo"
urlpatterns  = [path("", TaskListCreateView.as_view()),
				path("<int:pk>/", TaskDetailView.as_view()),
                path("signup", SignupView.as_view()),
                path("login", LoginView.as_view()),
				]
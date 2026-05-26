import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import todolist
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

@method_decorator(csrf_exempt, name = 'dispatch')
class TaskListCreateView(View):

    def get(self, request):
        try:
            breakpoint()
            user_id = request.GET.get('user_id')
            tasks = list(todolist.objects.filter(user_id = user_id).values())
            return JsonResponse(tasks, safe = False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request):
        breakpoint()
        try:
            data = json.loads(request.body)
            user_id = data.get('user')
            title = data.get('title')
            user = User.objects.filter(id = user_id).first()
            if not user:
                return JsonResponse(
                    {"message": "no user found"}, status = 400)
            if not title:
                return JsonResponse(
                    {"message": "Task not found"},status=400)
            existing_title = todolist.objects.filter(title=title, user = user).exists()
            if existing_title:
                return JsonResponse({"message" : "title already exists"}, status = 400)
            task = todolist.objects.create(title=data.get('title'),description=data.get('description'),completed=data.get('completed', False),user = user)
            return JsonResponse({
                "message": "Task created successfully",
                "id": task.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@method_decorator(csrf_exempt, name = 'dispatch')
class TaskDetailView(View):

    def get_object(self, pk,user_id):

        return todolist.objects.filter(id=pk, user_id = user_id).first()


    def get(self, request, pk):
        try:
            user_id = request.GET.get('user_id')
            task = self.get_object(pk, user_id)

            if not task:
                return JsonResponse(
                    {"message": "Task not found"},status=404)
            data = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id" : user_id,
                "created_on":task.created_on,
                "updated_on" : task.updated_on}
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    def delete(self, request, pk):
        try:
            user_id = request.GET.get('user_id')
            task = self.get_object(pk, user_id)

            if not task:
                return JsonResponse({"message": "Task not found"},status=404)

            task.delete()
            return JsonResponse({"message": "Task deleted successfully" })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    
    def patch(self, request, pk):
        try: 
            data = json.loads(request.body)
            user_id = data.get('user_id')
            task = self.get_object(pk, user_id)
            if not task:
                return JsonResponse({"message": "Task not found"},status=404)
            

            if 'title' in data:
                existing_task = todolist.objects.filter(title=data['title']).exclude(id=pk).exists()
                if existing_task:
                    return JsonResponse({"message": "Title already exists"}, status=400)
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'completed' in data:
                task.completed = data['completed']

            task.save()
            return JsonResponse({"message": "Task updated successfully" })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):

    def post(self, request):

        try:

            data = json.loads(request.body)

            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            # VALIDATIONS
            if not username:
                return JsonResponse({
                "message": "Username is required"
                }, status=400)

            if not password:
                return JsonResponse({
                "message": "Password is required"
                }, status=400)
            # CHECK USERNAME EXISTS
            if User.objects.filter(
                username=username
                ).exists():
                return JsonResponse({
                "message": "Username already exists"
                }, status=400)
            # CREATE USER
            user = User.objects.create_user(
            username=username,
            email=email,
            password=password
            )

            return JsonResponse({
            "message": "User created successfully",
            "user_id": user.id
            })

        except Exception as e:
            return JsonResponse({
            "error": str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        breakpoint()
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username,password=password)


            if user:

                return JsonResponse({
                "message": "Login successful",
                "user_id": user.id,
                "username": user.username
                })

            return JsonResponse({
            "message": "Invalid username or password"
            }, status=401)

        except Exception as e:

            return JsonResponse({
            "error": str(e)
            }, status=500)


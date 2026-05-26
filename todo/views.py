import json

from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect
)

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import (
    authenticate,
    login
)

from django.contrib.auth import get_user_model

from .models import todolist


User = get_user_model()



'''handels signup of a user
POST : DB entries of the new user 
validates the duplicate check '''
def signup_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email:
            return JsonResponse({
            "message": "EMAIL is required"
            }, status=400)
        if User.objects.filter(
            email=email).exists():
            return redirect('/todo/login/')
        
        if not username:
            return JsonResponse({
            "message": "Username is required"
            }, status=400)
        if not username.isalnum():
            return JsonResponse({
            "message": "specail character not allowed"
            }, status=400)
        if username[0].isdigit():
            return JsonResponse({
            "message": "do not start with number"
            }, status=400)
        
        if not password:
            return JsonResponse({
            "message": "Password is required"
            }, status=400)
        if password.isdigit() or len(password) < 8 or not any(char in "@#" for char in password):
            return JsonResponse({
            "message": "Password must be at least 8 characters long, not be entirely numeric, and include at least one special character (@ or #)."
            }, status=400)
        if User.objects.filter(
            username=username
            ).exists():
            return JsonResponse({
            "message": "Username already exists"
            }, status=400)
        
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/todo/login/')

    return render(
        request,
        'todo/signup.html'
    )


'''handles user login
fetches user info and authenticate'''
def login_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect(
                f'/todo/home/?user_id={user.id}'
            )

    return render(
        request,
        'todo/login.html'
    )


'''contains the todo list for each user.
provides the option to perform CRUD'''
def home_page(request):

    user_id = request.GET.get('user_id')

    tasks = todolist.objects.filter(
        user_id=user_id
    )

    return render(
        request,
        'todo/home.html',
        {'tasks': tasks}
    )


'''CSRF ensures the POST,PATCH,DELETE works propely.'''
@method_decorator(csrf_exempt, name='dispatch')
class TaskListCreateView(View):

    def get(self, request):  

        try:

            user_id = request.GET.get(
                'user_id'
            )

            tasks = list(
                todolist.objects.filter(
                    user_id=user_id
                ).values()
            )

            return JsonResponse(
                tasks,
                safe=False
            )

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)


    def post(self, request):
# used to create a new todo list 
        try:

           
            if request.content_type.startswith(
                'application/x-www-form-urlencoded'
            ):

                data = request.POST

            else:

                data = json.loads(
                    request.body
                )

            user_id = data.get('user')

            title = data.get('title')

            user = User.objects.filter(
                id=user_id
            ).first()

            if not user:

                return JsonResponse({
                    "message": "No user found"
                }, status=400)

            existing_title = todolist.objects.filter(
                title=title,
                user=user
            ).exists()

            if existing_title:

                return JsonResponse({
                    "message": "Title already exists"  # checks if title is already there 
                }, status=400)

            todolist.objects.create(
                title=title,
                description=data.get(
                    'description'
                ),
                completed=data.get(
                    'completed',
                    False
                ),
                user=user
            )

            return redirect(
                f'/todo/home/?user_id={user.id}'
            )

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)

'''handles single todo operations
PATCH : Updates a single todo list
GET : fetches a single todo list
DELETE : deletes the todo list '''

@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):
    def get_object(self, pk, user_id):

        return todolist.objects.filter(
            id=pk,
            user_id=user_id
        ).first()

    
    def post(self, request, pk):

        method = request.POST.get(
            '_method'
        )

        
        if method == 'PATCH':

            request._body = json.dumps({

                "user_id": request.POST.get(
                    'user_id'
                ),

                "title": request.POST.get(
                    'title'
                ),

                "description": request.POST.get(
                    'description'
                ),

                "completed": (
                    request.POST.get(
                        'completed'
                    ) == 'on'
                )

            }).encode('utf-8')

            return self.patch(
                request,
                pk
            )

        
        elif method == 'DELETE':

            request._body = json.dumps({

                "user_id": request.POST.get(
                    'user_id'
                )

            }).encode('utf-8')

            return self.delete(
                request,
                pk
            )

   
    def get(self, request, pk):

        try:

            user_id = request.GET.get(
                'user_id'
            )

            task = self.get_object(
                pk,
                user_id
            )

            if not task:

                return JsonResponse({
                    "message": "Task not found"
                }, status=404)

            data = {

                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": user_id,
                "created_on": task.created_on,
                "updated_on": task.updated_on
            }

            return JsonResponse(data)

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)

   
    def patch(self, request, pk):

        try:

            data = json.loads(
                request.body
            )

            user_id = data.get(
                'user_id'
            )

            task = self.get_object(
                pk,
                user_id
            )

            if not task:

                return JsonResponse({
                    "message": "Task not found"
                }, status=404)

            if 'title' in data:

                existing_task = todolist.objects.filter(
                    title=data['title']
                ).exclude(
                    id=pk
                ).exists()

                if existing_task:

                    return JsonResponse({
                        "message": "Title already exists"
                    }, status=400)

                task.title = data['title']

            if 'description' in data:

                task.description = data[
                    'description'
                ]

            if 'completed' in data:

                task.completed = data[
                    'completed'
                ]

            task.save()

            return redirect(
                f'/todo/home/?user_id={user_id}'
            )

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)

    
    def delete(self, request, pk):

        try:

            data = json.loads(
                request.body
            )

            user_id = data.get(
                'user_id'
            )

            task = self.get_object(
                pk,
                user_id
            )

            if not task:

                return JsonResponse({
                    "message": "Task not found"
                }, status=404)

            task.delete()

            return redirect(
                f'/todo/home/?user_id={user_id}'
            )

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)
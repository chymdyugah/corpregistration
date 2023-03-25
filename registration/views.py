from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

MyUser = get_user_model()

# Create your views here.


class RegisterView(View):
    template_name = 'register.html'
    
    def post(self, request):
        try:
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2:
                user = MyUser(username=username)
                user.set_password(password1)
                user.save()
            else:
                err = "Passwords are not the same"
                raise Exception(err)

            return redirect('users:emp_dashboard')
        except IntegrityError:
            err = "User Already Exists with that email"
            messages.error(request, err)
            return render(request, self.template_name)
        except Exception as e:
            messages.error(request, str(e))
            
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return render(request, self.template_name)

    @transaction.atomic
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            user.last_login = timezone.now()
            messages.success(request, f'Welcome back, {username.upper()}')
            return redirect('users:emp_dashboard')
        
        # send back a message
        messages.error(request, 'username or password incorrect.')
        return render(request, self.template_name)

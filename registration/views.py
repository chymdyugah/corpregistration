from django.shortcuts import render, redirect
from django.views.generic import ListView, View, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .models import CorpMember

MyUser = get_user_model()

# Create your views here.


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request):
        try:
            username = request.POST['username']
            password1 = request.POST['password']
            user = MyUser(username=username)
            user.set_password(password1)
            user.save()

            return redirect('registration:login')
        except IntegrityError:
            err = "User Already Exists with that username"
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
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('registration:list_corpmember')
        
        # send back a message
        messages.error(request, 'username or password incorrect.')
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('registration:login')


@method_decorator(login_required, name='dispatch')
class ListCorpMemberView(ListView):
    template_name = 'view-corp.html'
    context_object_name = 'corp_members'

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return CorpMember.objects.all()
        else:
            return CorpMember.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class CreateCorpMembersView(View):
    queryset = CorpMember.objects.all()
    template_name = 'register-corp.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        state_code = request.POST.get('state_code')
        phone = request.POST.get('phone')
        ppa = request.POST.get('ppa')
        call_up = request.POST.get('call_up')
        batch = request.POST.get('batch')
        stream = request.POST.get('stream')

        CorpMember.objects.create(
            user=request.user,
            name=name, 
            state_code=state_code, 
            phone=phone, 
            ppa=ppa, 
            call_up=call_up, 
            batch=batch, 
            stream=stream
        )

        messages.success(request, "Registration successful!")
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class UpdateCorpMemberView(View):
    template_name = 'edit-corp.html'

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return CorpMember.objects.all()
        else:
            return CorpMember.objects.filter(user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().get(id=kwargs.get('pk'))
        return render(request, self.template_name, {'corpmember': obj})
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        state_code = request.POST.get('state_code')
        phone = request.POST.get('phone')
        call_up = request.POST.get('call_up')
        batch = request.POST.get('batch')
        stream = request.POST.get('stream')
        CorpMember.objects.filter(id=kwargs.get('pk')).update(
            name=name, 
            phone=phone, 
            call_up=call_up, 
            state_code=state_code, 
            batch=batch, 
            stream=stream
        )
        obj = self.get_queryset().get(id=kwargs.get('pk'))
        messages.success(request, "Update successful")
        return redirect('registration:list_corpmember')


@method_decorator(login_required, name='dispatch')
class DeleteCorpMemberView(DeleteView):
    success_url = reverse_lazy('registration:list_corpmember')

    def get_queryset(self):
        if self.request.user.is_staff is True:
            return CorpMember.objects.all()
        else:
            return CorpMember.objects.filter(user=self.request.user)


class RedirectHomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('registration:login')

def page404(request, exception=None):
	template_name = "page404.html"
	return render(request, template_name, status=404)

def page500(request, exception=None):
	template_name = "page500.html"
	return render(request, template_name, status=500)
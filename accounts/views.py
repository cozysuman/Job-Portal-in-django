from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView
from accounts.forms import *
from accounts.models import User, Profile


class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'accounts/employee/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)
        # if form.is_valid():
        #     user = form.save(commit=False)
        #     password = form.cleaned_data.get("password1")
        #     user.set_password(password)
        #     user.is_active = True
        #     user.save()
        #     return redirect('accounts:login')
        # else:
        #     return render(request, 'accounts/employee/register.html', {'form': form})

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            context1 = {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                }
            message = render_to_string("acc_active_email.html", context1)
            mail_subject = "Activate your  account."
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('An activation link has been sent to your email.Please confirm your email address to complete the registration rightaway before the link expires.')





        else:
            return render(request, 'accounts/employee/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('accounts:login')
    else:
        return HttpResponse('Activation link is invalid!')



def profile(request):
    p_form=ProfileUpdateForm(request.POST or None)
    if request.method == 'POST':
        # u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('jobs:home')

    else:
        # u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm( request.POST, request.FILES,instance=request.user.profile)

    context = {
        # 'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'jobs/employee/profile.html', context)
# def company(request):


class RegisterEmployerView(CreateView):
    model = User
    form_class = EmployerRegistrationForm
    template_name = 'accounts/employer/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        # if form.is_valid():
        #     user = form.save(commit=False)
        #     password = form.cleaned_data.get("password1")
        #     user.set_password(password)
        #     user.save()
        #     return redirect('accounts:login')
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            context1 = {
                'user':user,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                }
            message = render_to_string("acc_active_email.html", context1)
            mail_subject = "Activate your  account."
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('An activation link has been sent to your email.Please confirm your email address to complete the registration rightaway before the link expires.')
        else:
            return render(request, 'accounts/employer/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)

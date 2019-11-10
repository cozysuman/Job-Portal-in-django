from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.decorators import user_is_employee
from accounts.forms import *



from django.views.generic import  ListView
from jobsapp.models import Job, Applicant
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Value



class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    success_url = reverse_lazy('accounts:employer-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj




class AppliedJobListView(ListView):
    model = Job
    template_name = 'jobs/employee/all-appliedjobs.html'
    context_object_name = 'appliedjobs'


    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        applied_jobs = Applicant.objects.values_list('job__id',flat = True).filter(user= self.request.user)
        return self.model.objects.filter(id__in =applied_jobs)

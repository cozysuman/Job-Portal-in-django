from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView,UpdateView

from jobsapp.decorators import user_is_employer, company_can_post
from jobsapp.forms import CreateJobForm, CreateCompanyForm, UpdateJobForm
from jobsapp.models import Job, Applicant , Company
from django.core.exceptions import PermissionDenied


from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin

from fuzzywuzzy import process
from curriculum.models import Resume

class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'


    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context

class FilterApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)



    def get_queryset(self):
        if self.request.GET['skill']:
            skillset= Resume.objects.all().values_list('skills__skill',flat=True)
            queryskill = self.request.GET['skill']
            tuple1= process.extractOne(queryskill, skillset,score_cutoff=80)
            if tuple1== None :
                queried_skill_match ='msdfnmasnfmnsfmn'
            else:
                queried_skill_match = tuple1[0]

        else:
            queried_skill_match=self.request.GET['skill']

        return Applicant.objects.filter(job_id=self.kwargs['job_id'],user__skills__skill__icontains=queried_skill_match).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context

# class JobCreateView(CreateView):
#     template_name = 'jobs/create.html'
#     form_class = CreateJobForm
#     extra_context = {
#         'title': 'Post New Job'
#     }
#     success_url = reverse_lazy('jobs:employer-dashboard')

#     @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
#     @method_decorator(user_is_employer)
#     @method_decorator(company_can_post)
#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return reverse_lazy('accounts:login')
#         if self.request.user.is_authenticated and self.request.user.role != 'employer':
#             return reverse_lazy('accounts:login')
#         return super().dispatch(self.request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.instance.company_name = Company.objects.values_list('company_name', flat=True ).get(user=self.request.user)
#         form.instance.company_description = Company.objects.values_list('company_description', flat=True ).get(user=self.request.user)
#         form.instance.website = Company.objects.values_list('website', flat=True ).get(user=self.request.user)
#         return super(JobCreateView, self).form_valid(form)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


#     def get_object(self , *args , **kwargs):
#         try:
#                 job = Job.objects.get(user=self.request.user)
#         except:
#                 job = None
#         return job


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    @method_decorator(company_can_post)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_name = Company.objects.values_list('company_name', flat=True ).get(user=self.request.user)
        form.instance.company_description = Company.objects.values_list('company_description', flat=True ).get(user=self.request.user)
        form.instance.website = Company.objects.values_list('website', flat=True ).get(user=self.request.user)
        return super(JobCreateView, self).form_valid(form)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_object(self , *args , **kwargs):

        job = None
        return job

    # def get_queryset(self,request):
    #     return self.User.objects.filter(email=request.user)





class CompanyCreateView(CreateView):
    template_name = 'jobs/create_company.html'
    form_class = CreateCompanyForm
    extra_context = {
        'title': 'Create Company Profile'
    }
    success_url = reverse_lazy('jobs:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company_name = self.request.user.first_name
        form.instance.email = self.request.user.email
        form.instance.address = self.request.user.last_name
        return super(CompanyCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class CompanyUpdateView(UpdateView):
    model = Company
    fields = ['company_description','website','Phone']
    template_name = 'jobs/update_companyprofile.html'
    success_url = reverse_lazy('jobs:home')

    def get_object(self, queryset=None):
        obj = Company.objects.get(user=self.request.user)
        if obj is None:
            raise Http404("Company doesn't exists")
        return obj


class JobUpdateView(SuccessMessageMixin, UpdateView):
    model=Job
    template_name = 'jobs/update_job.html'
    form_class = UpdateJobForm
    context_object_name = 'job'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('jobs:employer-dashboard')
    # success_message = "Job is updated successfully"

    # def get_object(self, queryset=None):
    #     obj = super(JobUpdateView, self).get_object(queryset=queryset)
    #     if obj is None:
    #         raise Http404("Job doesn't exists")
    #     return obj

    def get_object(self, queryset=None):

        obj = super(JobUpdateView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")

        elif obj.user == self.request.user:
            return obj
        else:
            raise PermissionDenied




    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_message(self, cleaned_data):
        #  cleaned_data is the cleaned data from the form which is used for string formatting
        return "Job is updated successfully"




class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id).distinct()


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    job.filled = True
    job.save()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))

# def company_profile_view(request):
#     """
#     Create a classic resume in :mod:`xhtml2pdf` format.
#     """
#     resume = get_object_or_404(Resume.objects.filter(user=request.user))
#     #resume=Resume.objects.get(firstname=first_name)
#     current_user = request.user
#     context = {
#         'pagesize': 'a4',
#         'resume': resume,
#         'skills': current_user.skills.order_by('category', '-weight'),
#         'projects': current_user.projects.order_by('-weight'),
#         'experiences': current_user.experiences.order_by('-start_year'),
#         'trainings': current_user.trainings.order_by('-start_year', '-start_month'),
#         'certifications': current_user.certifications.order_by('-end_year', '-end_month'),
#     }
#    # return get_template('curriculum/test1.html').render(context)
#     return render(request,'jobs/company_profile.html',context)
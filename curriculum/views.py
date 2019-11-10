"""
Views that can used by developer for easily export resume as PDF.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from curriculum import export
from curriculum import models
from curriculum.models import Resume,ProjectItem,SkillItem,CertificationItem,Training,Experience, LanguageItem
from accounts.models import User
from django.template.loader import get_template
from curriculum.forms import LanguageItemForm, ResumeForm, SkillItemForm, CertificationItemForm, ExperienceForm, ProjectItemForm, TrainingForm, LanguageFormset, SkillFormset, UpdateResumeForm, UpdateTrainingForm,UpdateSkillitemForm, UpdateProjectitemForm, UpdateExperienceForm,UpdateLanguageitemForm, UpdateCertificationitemForm

from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from jobsapp.decorators import user_can_search,user_is_employer,user_is_superuser,user_is_employee
from django.core.exceptions import PermissionDenied


@login_required(login_url=reverse_lazy('accounts:login'))
def export_single_page(request):
    """Get a resume in a single page PDF."""
    #resume = get_object_or_404(Resume.objects.filter(firstname='Vijay'))
    current_user=request.user
    try:
        pdf, result = export.export_pdf(current_user, export.single_page)
        raw_pdf = result.getvalue()
        if not pdf.err:
            return HttpResponse(raw_pdf, content_type='application/pdf')
        return HttpResponse('We had some errors.')
    except:
        return render(request,'Errors/CV_error.html')

@login_required(login_url=reverse_lazy('accounts:login'))
def export_classic(request):
    """Get a resume in a PDF with classic format."""
    #resume = get_object_or_404(Resume.objects.filter(id=resume_id))
    #resume = get_object_or_404(Resume.objects.filter(user=request.user))
    current_user=request.user

    try:
        pdf, result = export.export_pdf(current_user, export.classic)
        raw_pdf = result.getvalue()
        if not pdf.err:
            return HttpResponse(raw_pdf, content_type='application/pdf')
        return HttpResponse('We had some errors.')
    except:
        return render(request,'Errors/CV_error.html')

@login_required(login_url=reverse_lazy('accounts:login'))
def export_classic2(request):
    """Get a resume in a PDF with classic format."""
    #resume = get_object_or_404(Resume.objects.filter(id=resume_id))
    #resume = get_object_or_404(Resume.objects.filter(user=request.user))
    current_user=request.user
    try:
        pdf, result = export.export_pdf(current_user, export.classic2)
        raw_pdf = result.getvalue()
        if not pdf.err:
            return HttpResponse(raw_pdf, content_type='application/pdf')
        return HttpResponse('We had some errors.')
    except:
        return render(request,'Errors/CV_error.html')

@login_required(login_url=reverse_lazy('accounts:login'))
def export_classic1(request):
    """Get a resume in a PDF with classic format."""
    #resume = get_object_or_404(Resume.objects.filter(id=resume_id))
    #resume = get_object_or_404(Resume.objects.filter(firstname='Vijay'))
    current_user=request.user
    try:
        pdf, result = export.export_pdf(current_user, export.classic1)
        raw_pdf = result.getvalue()
        if not pdf.err:
            return HttpResponse(raw_pdf, content_type='application/pdf')
        return HttpResponse('We had some errors.')
    except:
        return render(request,'Errors/CV_error.html')

@login_required(login_url=reverse_lazy('accounts:login'))
def export_class(request):
    """
    Create a classic resume in :mod:`xhtml2pdf` format.
    """
    try:
        resume = get_object_or_404(Resume.objects.filter(user=request.user))
        current_user = request.user
        context = {
            'pagesize': 'a4',
            'resume': resume,
            'skills': current_user.skills.order_by('category'),
            'projects': current_user.projects.order_by('-weight'),
            'experiences': current_user.experiences.order_by('-start_year'),
            'trainings': current_user.trainings.order_by('-start_year', '-start_month'),
            'certifications': current_user.certifications.order_by('-end_year', '-end_month'),
        }
        return render(request,'curriculum/cvpreview.html',context)
    except:
        return render(request,'Errors/profile_error.html')




@login_required(login_url=reverse_lazy('accounts:login'))
def profileView(request):
    """
    Create a classic resume in :mod:`xhtml2pdf` format.
    """
    try:
        resume = get_object_or_404(Resume.objects.filter(user=request.user))
        current_user = request.user
        context = {
            'pagesize': 'a4',
            'resume': resume,
            'skills': current_user.skills.order_by('category'),
            'projects': current_user.projects.order_by('-weight'),
            'experiences': current_user.experiences.order_by('-start_year'),
            'trainings': current_user.trainings.order_by('-start_year', '-start_month'),
            'certifications': current_user.certifications.order_by('-end_year', '-end_month'),
            'language':current_user.languages.order_by('level'),
        }
        return render(request,'curriculum/profileview.html',context)
    except:
        return render(request,'Errors/profile_error.html')

"""
def skillitem(request):
    if request.method=="POST":
        form=ExperienceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect()
            except:
                pass
    else:
        form=ExperienceForm()
    return render(request,"producttemp.html",{'form':form})
"""


# @login_required(login_url=reverse_lazy('accounts:login'))
# def addlanguageitem(request):
#     if request.method == 'POST':
#         language = request.POST.getlist('language')
#         print(language)
#     form=LanguageItemForm(request.POST or None)
#     try:
#         if form.is_valid():
#             instance=form.save(commit=False)
#             instance.user=request.user
#             instance.resume= Resume.objects.get(user=request.user)
#             instance.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('curriculum:languageitem')

#         context={
#             'form':form,
#             'languageitem_active':"active"
#         }
#         return render(request,"curriculum/languageitem.html",context)
#     except ObjectDoesNotExist:
#         messages.success(request, f'Please create resume before you add in details')
#         return redirect('curriculum:resume')


@login_required(login_url=reverse_lazy('accounts:login'))
def addlanguageitem(request):
    template_name = 'curriculum/languageitem.html'
    # heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LanguageFormset(queryset=models.LanguageItem.objects.filter(user=request.user))
    if request.method == 'POST':
        formset = LanguageFormset(request.POST)
        try:

            if formset.is_valid():
                for form in formset:
                # only save if name is present
                    if form.cleaned_data.get('language'):
                        instance=form.save(commit=False)
                        instance.user=request.user
                        instance.resume= Resume.objects.get(user=request.user)
                        instance.save()
                return redirect('curriculum:languageitem')
        except IntegrityError:
            messages.success(request, f'You have already added that language!!!')
            return redirect('curriculum:languageitem')
        except ObjectDoesNotExist:
            messages.success(request, f'Please create resume before you add in details')
            return redirect('curriculum:resume')

    return render(request, template_name, {
        'formset': formset,
        'languageitem_active':"active",
    })

@login_required(login_url=reverse_lazy('accounts:login'))
def addresume(request):
    form=ResumeForm(request.POST or None, request.FILES)
    obj=User.objects.filter(email=request.user)
    # instance.user=request.user
    try:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            # print(instance.user)
            instance.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('curriculum:training')

        context={
            'form':form,
            'obj':obj,
            'resume_active':"active"
        }
        return render(request,"curriculum/resume.html",context)
    except IntegrityError:
        #return HttpResponse("ERROR!!! You have already filled your basic information. Go to update CV in update profile to change information")
        messages.success(request, f'You are trying to  create new instance of your resume when you already have one. You cannot do that, please make changes to your resume here')
        return redirect('curriculum:updateResume')






# @login_required(login_url=reverse_lazy('accounts:login'))
# def addskillitem(request):
#     form=SkillItemForm(request.POST or None, request.FILES)
#     try:
#         if form.is_valid():
#             instance=form.save(commit=False)
#             instance.user=request.user
#             instance.resume= Resume.objects.get(user=request.user)
#             instance.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('curriculum:skillitem')

#         context={
#         'form':form,
#         'skillitem_active':"active"
#         }
#         return render(request,"curriculum/skillitem.html",context)
#     except IntegrityError:
#         messages.success(request, f'You alraedy have that skill!!!')
#         return redirect('curriculum:skillitem')
#     except ObjectDoesNotExist:
#         messages.success(request, f'Please create resume before you add in details')
#         return redirect('curriculum:resume')





@login_required(login_url=reverse_lazy('accounts:login'))
def addskillitem(request):
    template_name = 'curriculum/skillitem.html'
    # heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = SkillFormset(queryset=models.SkillItem.objects.filter(user=request.user))
    elif request.method == 'POST':
        formset = SkillFormset(request.POST)
        try:
            if formset.is_valid():
                for form in formset:
                # only save if name is present
                    if form.cleaned_data.get('skill'):
                        instance=form.save(commit=False)
                        instance.user=request.user
                        instance.resume= Resume.objects.get(user=request.user)
                        instance.save()
                return redirect('curriculum:skillitem')
        except IntegrityError:
            messages.success(request, f'You already have that skill!!!')
            return redirect('curriculum:skillitem')
        except ObjectDoesNotExist:
            messages.success(request, f'Please create resume before you add in details')
            return redirect('curriculum:resume')


    return render(request, template_name, {
        'formset': formset,
        'skillitem_active':"active",
    })



@login_required(login_url=reverse_lazy('accounts:login'))
def addcertificationitem(request):
    form=CertificationItemForm(request.POST or None, request.FILES)
    try:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.resume= Resume.objects.get(user=request.user)
            instance.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('curriculum:languageitem')

        context={
            'form':form,
            'certificationitem_active':"active"
        }
        return render(request,"curriculum/certificationitem.html",context)
    except ObjectDoesNotExist:
        messages.success(request, f'Please create resume before you add in details')
        return redirect('curriculum:resume')

@login_required(login_url=reverse_lazy('accounts:login'))
def addexperience(request):
    form=ExperienceForm(request.POST or None, request.FILES)
    try:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.resume= Resume.objects.get(user=request.user)
            instance.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('curriculum:certificationitem')

        context={
            'form':form,
            'experience_active':"active"
        }
        return render(request,"curriculum/experience.html",context)
    except ObjectDoesNotExist:
        messages.success(request, f'Please create resume before you add in details')
        return redirect('curriculum:resume')

@login_required(login_url=reverse_lazy('accounts:login'))
def addprojectitem(request):
    form=ProjectItemForm(request.POST or None, request.FILES)
    try:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.resume= Resume.objects.get(user=request.user)
            instance.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('curriculum:projectitem')

        context={
            'form':form,
            'projectitem_active':"active"
        }
        return render(request,"curriculum/projectitem.html",context)
    except ObjectDoesNotExist:
        messages.success(request, f'Please create resume before you add in details')
        return redirect('curriculum:resume')

@login_required(login_url=reverse_lazy('accounts:login'))
def addtraining(request):
    form=TrainingForm(request.POST or None, request.FILES)
    try:
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.resume= Resume.objects.get(user=request.user)
            instance.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('curriculum:training')

        context={
            'form':form,
            'training_active':"active"
        }
        return render(request,"curriculum/training.html",context)
    except ObjectDoesNotExist:
        messages.success(request, f'Please create resume before you add in details')
        return redirect('curriculum:resume')

@login_required(login_url=reverse_lazy('accounts:login'))
def menulist(request,*args,**kwargs):
    return render(request,"resume_base.html",{})

@login_required(login_url=reverse_lazy('accounts:login'))
def resume_generate(request,*args,**kwargs):
    return render(request,"curriculum/resume_generate.html",{})


# def fullResume(request,*args,**kwargs):
#     resume_form=ResumeForm(request.POST or None, request.FILES)
#     skill_form=SkillForm(request.POST or None, request.FILES)
#     project_form=ProjectForm(request.POST or None, request.FILES)
#     # resume_form.fields["firstname"].queryset = User.objects.filter(id=1)
#     obj=User.objects.filter(email=request.user)
#     print(request.user)
#     print(obj)

#     context = {
#         'r_form':resume_form,
#         's_form':skill_form,
#         'p_form':project_form,
#         'obj':obj
#     }

#     return render(request, 'curriculum/profile.html', context)



def fullResume(request,*args,**kwargs):
    resume_form=UpdateResumeForm(request.POST or None, request.FILES,instance=request.user)
    # skill_form=SkillForm(request.POST or None, request.FILES)
    # project_form=ProjectForm(request.POST or None, request.FILES)
    # # resume_form.fields["firstname"].queryset = User.objects.filter(id=1)
    # obj=User.objects.filter(email=request.user)
    # print('sss')
    # print(obj.id)
    # print(obj)

    context = {
        'r_form':resume_form,
        's_form':skill_form,
        'p_form':project_form,
        # 'obj':obj
    }

    return render(request, 'curriculum/profile.html', context)




class EditProfileView(UpdateView):
    model = models.Resume
    form_class = UpdateResumeForm
    context_object_name = 'resume'
    template_name = 'curriculum/update/profile.html'
    success_url = reverse_lazy('curriculum:updateResume')

    # @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    # @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())


    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['resume_active'] = 'active'
        return context

    def get_object(self, queryset=None):
        # obj = self.request.user
        # obj = models.Resume.objects.filter(pk=self.kwargs['user_id'])
        obj = models.Resume.objects.filter(user=self.request.user)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj.first()




class TrainingListView(ListView):
    model = models.Training
    template_name = 'curriculum/update/traininglist.html'
    context_object_name = 'trainings'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['training_active'] = 'active'
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

class UpdateTrainingView(UpdateView):
    model = models.Training
    template_name = 'curriculum/update/training.html'
    form_class = UpdateTrainingForm
    success_url = reverse_lazy('curriculum:updatetraining')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    #@method_decorator(user_is_currentuser )
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        training= get_object_or_404(Training,id=id)
        if training.user== self.request.user:
            return training
        else:
            raise PermissionDenied
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['training_active'] = 'active'
        return context


class TrainingDeleteView(DeleteView):
    model = models.Training
    success_url = reverse_lazy('curriculum:updatetraining')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(Training,id=id)




class ProjectListView(ListView):
    model = models.ProjectItem
    template_name = 'curriculum/update/projectlist.html'
    context_object_name = 'projects'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['project_active'] = 'active'
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

class UpdateProjectView(UpdateView):
    model = models.ProjectItem
    template_name = 'curriculum/update/projectitem.html'
    form_class = UpdateProjectitemForm
    success_url = reverse_lazy('curriculum:updateproject')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        project= get_object_or_404(ProjectItem,id=id)
        if project.user== self.request.user:
            return project
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['project_active'] = 'active'
        return context

class ProjectDeleteView(DeleteView):
    model = models.ProjectItem
    success_url = reverse_lazy('curriculum:updateproject')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(ProjectItem,id=id)




class ExperienceListView(ListView):
    model = models.Experience
    template_name = 'curriculum/update/experiencelist.html'
    context_object_name = 'experiences'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['experience_active'] = 'active'
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)

class UpdateExperienceView(UpdateView):
    model = models.Experience
    template_name = 'curriculum/update/experience.html'
    form_class = UpdateExperienceForm
    success_url = reverse_lazy('curriculum:updateexperience')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        experience= get_object_or_404(Experience,id=id)
        if experience.user== self.request.user:
            return experience
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['experience_active'] = 'active'
        return context

class ExperienceDeleteView(DeleteView):
    model = models.Experience
    success_url = reverse_lazy('curriculum:updateexperience')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(Experience,id=id)




class SkillListView(ListView):
    model = models.SkillItem
    template_name = 'curriculum/update/skilllist.html'
    context_object_name = 'skills'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['skill_active'] = 'active'
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class UpdateSkillView(UpdateView):
    model = models.Training
    template_name = 'curriculum/update/skillitem.html'
    form_class = UpdateSkillitemForm
    success_url = reverse_lazy('curriculum:updateskill')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        skill= get_object_or_404(SkillItem,id=id)
        if skill.user== self.request.user:
            return skill
        else:
            raise PermissionDenied


    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['skill_active'] = 'active'
        return context


class SkillDeleteView(DeleteView):
    model = models.SkillItem
    success_url = reverse_lazy('curriculum:updateskill')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(SkillItem,id=id)

class CertificationListView(ListView):
    model = models.CertificationItem
    template_name = 'curriculum/update/certificationlist.html'
    context_object_name = 'certifications'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['certification_active'] = 'active'
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class UpdateCertificationView(UpdateView):
    model = models.CertificationItem
    template_name = 'curriculum/update/certificationitem.html'
    form_class = UpdateCertificationitemForm
    success_url = reverse_lazy('curriculum:updatecertification')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        certification= get_object_or_404(CertificationItem,id=id)
        if certification.user== self.request.user:
            return certification
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['certification_active'] = 'active'
        return context

class CertificationDeleteView(DeleteView):
    model = models.CertificationItem
    success_url = reverse_lazy('curriculum:updatecertification')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(CertificationItem,id=id)


class LanguageListView(ListView):
    model = models.LanguageItem
    template_name = 'curriculum/update/languagelist.html'
    context_object_name = 'languages'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['language_active'] = 'active'
        return context

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class UpdateLanguageView(UpdateView):
    model = models.LanguageItem
    template_name = 'curriculum/update/languageitem.html'
    form_class = UpdateLanguageitemForm
    success_url = reverse_lazy('curriculum:updatelanguage')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        language= get_object_or_404(LanguageItem,id=id)
        if language.user== self.request.user:
            return language
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
    # Add in the publisher
        context['language_active'] = 'active'
        return context

class LanguageDeleteView(DeleteView):
    model = models.LanguageItem
    success_url = reverse_lazy('curriculum:updatelanguage')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        return get_object_or_404(LanguageItem,id=id)

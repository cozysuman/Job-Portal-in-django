from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from django.contrib.staticfiles.templatetags.staticfiles import static
from curriculum import models
from django.forms import (formset_factory, modelformset_factory)

# from accounts import Profile



class ResumeExportForm(forms.Form):
    hide_image = forms.BooleanField(required=False)
    hide_resume = forms.BooleanField(required=False)

    hide_phone = forms.BooleanField(required=False)
    hide_city = forms.BooleanField(required=False)
    hide_country = forms.BooleanField(required=False)


    hide_email = forms.BooleanField(required=False)
    hide_website = forms.BooleanField(required=False)
    hide_skype = forms.BooleanField(required=False)
    hide_stackoverflow = forms.BooleanField(required=False)
    hide_github = forms.BooleanField(required=False)
    hide_experience_description = forms.BooleanField(required=False)
    hide_experience_environment = forms.BooleanField(required=False)
    hide_certification_description = forms.BooleanField(required=False)
    hide_training_description = forms.BooleanField(required=False)

    hide_project_url = forms.BooleanField(required=False)

    class Media:
        css = {'all': (static('admin/css/widgets.css'),), }

    def __init__(self, instance, *args, **kwargs):
        super(ResumeExportForm, self).__init__(*args, **kwargs)
        self.instance = instance
        self.fields['experiences'] = forms.ModelMultipleChoiceField(
            queryset=instance.experiences.all(),
            initial=instance.experiences.all(),
            widget=widgets.FilteredSelectMultiple(_("experiences"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['projects'] = forms.ModelMultipleChoiceField(
            queryset=instance.projects.all(),
            initial=instance.projects.all(),
            widget=widgets.FilteredSelectMultiple(_("projects"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['skills'] = forms.ModelMultipleChoiceField(
            queryset=instance.skills.order_by('skill'),
            initial=instance.skills.all(),
            widget=widgets.FilteredSelectMultiple(_("skills"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['certifications'] = forms.ModelMultipleChoiceField(
            queryset=instance.certifications.all(),
            initial=instance.certifications.all(),
            widget=widgets.FilteredSelectMultiple(_("certifications"), is_stacked=False,
                    attrs={'size': 5, 'style': 'height: unset'}))
        self.fields['trainings'] = forms.ModelMultipleChoiceField(
            queryset=instance.trainings.all(),
            initial=instance.trainings.all(),
            widget=widgets.FilteredSelectMultiple(_("trainings"), is_stacked=False,
                    attrs={'size': 3, 'style': 'height: unset'}))
        self.fields['languages'] = forms.ModelMultipleChoiceField(
            queryset=instance.languages.all(),
            initial=instance.languages.all(),
            widget=widgets.FilteredSelectMultiple(_("languages"), is_stacked=False,
                    attrs={'size': 4, 'style': 'height: unset'}))


# class ExperienceForm(forms.ModelForm):
#     class Meta:
#         model = models.Experience
#         exclude = ()

#     def clean(self):
#         cleaned_data = super(ExperienceForm, self).clean()
#         if cleaned_data.get('end_month') and not cleaned_data.get('end_year'):
#             raise forms.ValidationError(_(
#                 "You must specify an end year with end month."))
#         if cleaned_data.get('end_year'):
#             if cleaned_data.get('end_year') < cleaned_data.get('start_year'):
#                 raise forms.ValidationError(_("End year is lower than start."))
#         if cleaned_data.get('end_year') == cleaned_data.get('start_year'):
#             if cleaned_data.get('end_month') < cleaned_data.get('start_month'):
#                 raise forms.ValidationError(_("End month is lower than start."))

#     def clean_end_year(self):
#         data = self.cleaned_data['end_year']
#         if not self.cleaned_data['still'] and not data:
#             raise forms.ValidationError(_(
#                 "You must specify an end year if experience is finished."))
#         return data


class LanguageItemForm(forms.ModelForm):
    class Meta:
        model=models.LanguageItem
        fields=[
             'level','language'
        ]

# LanguageFormset = formset_factory(LanguageItemForm)
LanguageFormset = modelformset_factory(
    models.LanguageItem,
    fields=('language','level','id', ),
    extra=1,
    widgets={
        'language': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Language here'
            })
    }
)

SkillFormset = modelformset_factory(
    models.SkillItem,
    fields=('skill','level','category','id', ),
    extra=1,
    widgets={
        'skill': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Skill here'
            })
        # 'level': forms.TextInput(attrs={
        #     'class': 'form-control',
        #     'placeholder': 'Enter Language here'
        #     }
        # )
    }
)

class ResumeForm(forms.ModelForm):
    class Meta:
        model=models.Resume
        fields = '__all__'
        exclude = ('user',)


class SkillItemForm(forms.ModelForm):
    class Meta:
        model=models.SkillItem
        fields = '__all__'
        exclude = ('user','resume',)

    def __init__(self, *args, **kwargs):
        super(SkillItemForm, self).__init__(*args, **kwargs)
        self.fields['skill'].error_messages = {'required': ''}
        self.fields['level'].error_messages = {'required': ''}



class CertificationItemForm(forms.ModelForm):
    class Meta:
        model=models.CertificationItem
        fields = '__all__'
        exclude = ('user','resume',)

    def __init__(self, *args, **kwargs):
        super(CertificationItemForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages = {'required': ''}
        self.fields['authority'].error_messages = {'required': ''}
        self.fields['end_year'].error_messages = {'required': ''}

class ExperienceForm(forms.ModelForm):
    class Meta:
        model=models.Experience
        fields = '__all__'
        exclude = ('user','resume',)

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['title'].error_messages = {'required': ''}
        self.fields['entreprise'].error_messages = {'required': ''}
        self.fields['start_year'].error_messages = {'required': ''}
        self.fields['start_month'].error_messages = {'required': ''}
        self.fields['type'].error_messages = {'required': ''}






class ProjectItemForm(forms.ModelForm):
    class Meta:
        model=models.ProjectItem
        fields = '__all__'
        exclude = ('user','resume',)

    def __init__(self, *args, **kwargs):
        super(ProjectItemForm, self).__init__(*args, **kwargs)

        self.fields['title'].error_messages = {'required': ''}
        self.fields['weight'].error_messages = {'required': ''}
        self.fields['start_year'].error_messages = {'required': ''}
        self.fields['start_month'].error_messages = {'required': ''}

class TrainingForm(forms.ModelForm):
    class Meta:
        model=models.Training
        fields = '__all__'
        exclude = ('user','resume',)


    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['school'].error_messages = {'required': ''}
        self.fields['degree'].error_messages = {'required': ''}
        self.fields['start_year'].error_messages = {'required': ''}
        self.fields['start_month'].error_messages = {'required': ''}
        self.fields['field_of_study'].error_messages = {'required': ''}



class UpdateResumeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateResumeForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['middlename'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['lastname'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['title'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['resume'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['image'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['phone'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['website'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['city'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['country'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['hobbies'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['skype'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['github'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )

    class Meta:
        model = models.Resume
        fields = ["firstname", "middlename","lastname","title","resume","image","phone","website","email","city","country","hobbies","skype","github"]





class UpdateTrainingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateTrainingForm, self).__init__(*args, **kwargs)
        self.fields['school'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['degree'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )

        self.fields['field_of_study'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['result'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['start_year'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['start_month'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['end_year'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['end_month'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )

    class Meta:
        model = models.Training
        fields = ["school", "degree","field_of_study","result","start_year","start_month","end_year","end_month"]





class UpdateProjectitemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateProjectitemForm, self).__init__(*args, **kwargs)
        self.fields['start_year'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )


    class Meta:
        model = models.ProjectItem
        fields = ["title","url","description","start_year","end_year","end_month"]





class UpdateSkillitemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateSkillitemForm, self).__init__(*args, **kwargs)
        self.fields['level'].widget.attrs.update(
            {
                'input_type': 'select',
            }
        )


    class Meta:
        model = models.SkillItem
        fields = ["skill","level","category"]



class UpdateLanguageitemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateLanguageitemForm, self).__init__(*args, **kwargs)
        self.fields['level'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )


    class Meta:
        model = models.LanguageItem
        fields = ["language","level"]




class UpdateExperienceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateExperienceForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )


    class Meta:
        model = models.Experience
        fields = ["title","entreprise","description","start_year","end_year"]




class UpdateCertificationitemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateCertificationitemForm, self).__init__(*args, **kwargs)
        self.fields['end_year'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )


    class Meta:
        model = models.CertificationItem
        fields = ["title","authority","url","end_year"]



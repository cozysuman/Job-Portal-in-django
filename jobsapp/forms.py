from django import forms

from jobsapp.models import Job, Applicant, Company


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user', 'created_at','company_name','company_description','website',)

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('user','registered','company_name','email','address',)

    def is_valid(self):
        valid = super(CreateCompanyForm , self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        company = super(CreateCompanyForm, self).save(commit=False)
        if commit:
            company.save()
        return company

# class UpdateCompanyForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(UpdateCompanyForm, self).__init__(*args, **kwargs)

#         self.fields['company_description'].widget.attrs.update(
#             {
#                 'placeholder': '',
#             }
#         )
#         self.fields['website'].widget.attrs.update(
#             {
#                 'placeholder': '',
#             }
#         )
#         self.fields['Phone'].widget.attrs.update(
#             {
#                 'placeholder': '',
#             }
#         )

#     class Meta:
#         model = Company
#         fields = ["company_description", "website","Phone"]




class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)




class UpdateJobForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateJobForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': '',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'placeholder': 'lol',
            }
        )
        self.fields['last_date'].widget.attrs.update(
            {
                'input_type': 'date',
            }
        )


    class Meta:
        model = Job
        fields = ["title", "description", "location","last_date"]
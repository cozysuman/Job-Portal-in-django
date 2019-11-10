from django.db import models
from django.utils import timezone

from accounts.models import User
from django.core.validators import *
from django.utils.translation import ugettext_lazy as _

telephone = RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')


JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()

    skills=models.CharField(max_length=150,default=None)
    salary=models.CharField(max_length=150,default=None)
    negotiable = models.BooleanField(default=False)

    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.description[:100]

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='companies')
    company_name = models.CharField(max_length=100)
    #logo = models.ImageField(default='default.jpg', upload_to='company_images', blank=True, null=True, verbose_name=_("Company logo"))
    company_description = models.TextField(max_length=3000, blank=True, null=True, verbose_name=_("Commpany description"))
    website = models.CharField(max_length=100, default="")
    registered = models.BooleanField(default=False)

    email = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("email"))
    Phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Phone"))

    address = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Location"))

    def __str__(self):
        return self.company_name


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()
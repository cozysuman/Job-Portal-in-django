from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from curriculum.models.utils import YEARS, MONTHS
from curriculum.models import utils

from django.conf import settings

EDUCATION_LEVELS = (
    ('High School', _('High School')),
    ('Diploma', _('Diploma')),
    ('Bachelors', _('Bachelors')),
    ('Masters', _('Masters')),
    ('Phd', _('Phd')),
    ('SLC/SEE', _('SLC/SEE')),
    ('Others', _('Others')),
)
@python_2_unicode_compatible
class Training(models.Model):
    resume = models.ForeignKey("curriculum.Resume", related_name='trainings',on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='trainings',on_delete=models.CASCADE,default=None)

    school = models.CharField(max_length=150, verbose_name=_("school"))
    degree = models.CharField(max_length=150, choices=EDUCATION_LEVELS, verbose_name=_("level"))
    result = models.CharField(max_length=150, blank=True, verbose_name=_("result"),help_text=_("GPA or Percentage"))
    field_of_study = models.CharField(max_length=150,default=None,null=True, blank=True, verbose_name=_("Field of Study"),help_text=_("eg. Computer Engineering"))

    start_year = models.IntegerField(choices=utils.YEARS, null=True, blank=True, default=utils.current_year, verbose_name=_("start year"))
    start_month = models.IntegerField(choices=utils.MONTHS, null=True, blank=True, default=utils.current_month, verbose_name=_("start month"))

    end_year = models.IntegerField(choices=utils.YEARS, null=True, blank=True, verbose_name=_("end year"))
    end_month = models.IntegerField(choices=utils.MONTHS, null=True, blank=True, verbose_name=_("end month"))



    class Meta:
        app_label = 'curriculum'

    def __str__(self):
        return self.degree

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from curriculum.models import utils

from django.conf import settings

@python_2_unicode_compatible
class ProjectItem(models.Model):
    resume = models.ForeignKey("curriculum.Resume", related_name='projects',on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='projects',on_delete=models.CASCADE,default=None)
    title = models.CharField(max_length=200,  verbose_name=_("Project Title "),default=None)
    description = models.TextField(max_length=3000, blank=True, verbose_name=_("description"),default=None)
    url = models.URLField(max_length=300, blank=True, verbose_name=_("URL"),default=None)
    start_year = models.IntegerField(choices=utils.YEARS, null=True, blank=True, default=utils.current_year, verbose_name=_("start year"))
    start_month = models.IntegerField(choices=utils.MONTHS, null=True, blank=True, default=utils.current_month, verbose_name=_("start month"))
    still = models.BooleanField(default=True, verbose_name=_("still contributor"))
    end_year = models.IntegerField(choices=utils.YEARS, null=True, blank=True, verbose_name=_("end year"))
    end_month = models.IntegerField(choices=utils.MONTHS, null=True, blank=True, verbose_name=_("end month"))

    weight = models.IntegerField(choices=utils.WEIGHTS, default=1, verbose_name=_("weight"))

    class Meta:
        app_label = 'curriculum'

    def __str__(self):
        return self.title

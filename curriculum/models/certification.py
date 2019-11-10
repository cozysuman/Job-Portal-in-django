from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from curriculum.models.utils import YEARS, MONTHS

from django.conf import settings



@python_2_unicode_compatible
class CertificationItem(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("title"),default=None)
    authority = models.CharField(max_length=200, verbose_name=_("authority"),default=None,help_text=_("eg. Google"))
    url = models.URLField(max_length=300, blank=True, verbose_name=_("URL"),default=None)

    resume = models.ForeignKey("curriculum.Resume", related_name='certifications',on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='certifications',on_delete=models.CASCADE,default=None)

    end_year = models.IntegerField(choices=YEARS, verbose_name=_("Certified year"))
    end_month = models.IntegerField(choices=MONTHS, null=True, blank=True, verbose_name=_("Certified month"))

    class Meta:
        app_label = 'curriculum'
        

    def __str__(self):
        return _('%(title)s at %(authority)s') % \
                {'title': self.title, 'authority': self.authority}

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from curriculum.models import utils

from django.conf import settings
SKILL_LEVELS = (
    (None, _('unknown')),
    ('B', _('beginner')),
    ('S', _('skilled')),
    ('A', _('advanced')),
    ('E', _('expert')),
)




@python_2_unicode_compatible
class SkillItem(models.Model):
    resume = models.ForeignKey("curriculum.Resume", related_name='skills',on_delete=models.CASCADE,default=None)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='skills',on_delete=models.CASCADE,default=None)

    skill = models.CharField(max_length=200,verbose_name=_("name"),default=None)
    level = models.CharField(max_length=1, choices=SKILL_LEVELS, verbose_name=_("level"))
    category = models.CharField(max_length=50, blank=True, verbose_name=_("category"))

    class Meta:
        app_label = 'curriculum'
        unique_together = ('skill', 'user')

    def __str__(self):
        return self.skill

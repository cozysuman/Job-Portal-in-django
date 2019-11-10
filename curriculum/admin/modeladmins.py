from django.contrib import admin
from curriculum import models, forms
from curriculum.admin import actions


class ResumeAdmin(admin.ModelAdmin):
    actions = (actions.export_resume,)
    list_display = ('firstname', 'lastname', 'title')
    list_filter=('title','city','trainings',)
    search_fields= ('skills__skill','title','firstname',)
    fieldsets = (
        (None, {
            'fields': (
                ('firstname', 'lastname', 'title'),
                ('user', 'image'),
                ('phone', 'email', 'website'),
                ('country', 'city'),

                ( 'skype', 'stackoverflow', 'github'),
                ('hobbies'),

            )
        }),
    )



class CertificationItemAdmin(admin.ModelAdmin):
    # list_display = ('certification', 'user')
    fieldsets = (
        (None, {
            'fields': (
                'user',

                ('end_year', 'end_month'),
            )
        }),
    )


class ExperienceAdmin(admin.ModelAdmin):
    form = forms.ExperienceForm
    list_display = ('title', 'entreprise', 'start_year', 'start_month',
                    'end_year', 'end_month',
                    'user'
                   )
    fieldsets = (
        (None, {
            'fields': (

                ('title', 'entreprise', 'type'),
                'description',
                ('start_year', 'start_month', 'still'),
                ('end_year', 'end_month'),

            )
        }),
    )




class LanguageItemAdmin(admin.ModelAdmin):
    list_display = ('language', 'level', 'user')
    fieldsets = (
        (None, {
            'fields': (
                'user',
                ('language', 'level'),
            )
        }),
    )

class ProjectItemAdmin(admin.ModelAdmin):
    # list_display = ('user')
    search_fields=('title',)
    fieldsets = (
        (None, {
            'fields': (
                'user',
                'title',

                ('start_year', 'start_month', 'still'),
                ('end_year', 'end_month'),
                'weight'
            )
        }),
    )




class SkillItemAdmin(admin.ModelAdmin):
    list_display = ('skill', 'level', 'category', 'user')
    list_per_page = 200
    fieldsets = (
        (None, {
            'fields': (
                'user',
                ('skill', 'level', 'category'),

            )
        }),
    )


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('degree', 'school', 'user')
    fieldsets = (
        (None, {
            'fields': (
                'user',
                ('degree', 'school'),
                'result',
                ('start_year', 'start_month'),
                ('end_year', 'end_month'),

            )
        }),
    )


admin.site.register(models.Resume, ResumeAdmin)
admin.site.register(models.CertificationItem, CertificationItemAdmin)
admin.site.register(models.Experience, ExperienceAdmin)
admin.site.register(models.LanguageItem, LanguageItemAdmin)
admin.site.register(models.ProjectItem, ProjectItemAdmin)
admin.site.register(models.SkillItem, SkillItemAdmin)
admin.site.register(models.Training, TrainingAdmin)

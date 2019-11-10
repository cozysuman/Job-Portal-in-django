from django.contrib import admin
from . models import Job, Applicant, Company


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_filter=('registered',)
    search_fields= ('company_name',) 

class JobAdmin(admin.ModelAdmin):
	list_display = ('title', 'company_name')
	list_filter=('type','company_name','title',)
	search_fields= ('skills','title',)
   




admin.site.register(Job, JobAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Applicant)
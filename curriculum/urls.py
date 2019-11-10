from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from .views import *


app_name = "curriculum"

urlpatterns = [
    
    path('classic/',export_classic,name='classic'),
    path('classic1/',export_classic1,name='classic1'),
    path('modern/',export_single_page,name='modern'),
    #path('htmltest/<str:first_name>/',export_class,name='test'),
    path('viewCV/',export_class,name='viewCV'),
    path('profileview/',profileView,name='profileview'),
    path('htmltest/',export_classic2,name='test'),

    
    path('languageitem/',addlanguageitem,name='languageitem'),
    path('resume/',addresume,name='resume'),
    # path('skill/',addskill,name='skill'),
    path('skillitem/',addskillitem,name='skillitem'),
    # path('certification/',addcertification,name='certification'),
    path('certificationitem/',addcertificationitem,name='certificationitem'),
    path('experience/',addexperience,name='experience'),
    # path('project/',addproject,name='project'),
    path('projectitem/',addprojectitem,name='projectitem'),
    path('training/',addtraining,name='training'),
    path('cv/',resume_generate,name='resume_generate'),
    path('edit_profile/',menulist,name='showmenu'),
    path('updateresume/',EditProfileView.as_view(),name='updateResume'),
    

    path('updatetraining/',TrainingListView.as_view(),name='updatetraining'),
    path('updatetraining/<int:id>', UpdateTrainingView.as_view(), name='update_training'),
    path('deletetraining/<int:id>', TrainingDeleteView.as_view(), name='delete_training'),

    path('updateskill',SkillListView.as_view(),name='updateskill'),
    path('updateskill/<int:id>', UpdateSkillView.as_view(), name='update_skill'),
    path('deleteskill/<int:id>', SkillDeleteView.as_view(), name='delete_skill'),


    path('updateproject',ProjectListView.as_view(),name='updateproject'),
    path('updateproject/<int:id>', UpdateProjectView.as_view(), name='update_project'),
    path('deleteproject/<int:id>', ProjectDeleteView.as_view(), name='delete_project'),





    path('updatelanguage',LanguageListView.as_view(),name='updatelanguage'),
    path('updatelanguage/<int:id>', UpdateLanguageView.as_view(), name='update_language'),
    path('deletelanguage/<int:id>', LanguageDeleteView.as_view(), name='delete_language'),


    path('updateexperience',ExperienceListView.as_view(),name='updateexperience'),
    path('updateexperience/<int:id>', UpdateExperienceView.as_view(), name='update_experience'),
    path('deleteexperience/<int:id>', ExperienceDeleteView.as_view(), name='delete_experience'),


    path('updatecertification',CertificationListView.as_view(),name='updatecertification'),
    path('updatecertification/<int:id>', UpdateCertificationView.as_view(), name='update_certification'),
    path('deletecertification/<int:id>', CertificationDeleteView.as_view(), name='delete_certification'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from haystack import indexes
from curriculum.models import Resume,SkillItem,Experience,Project,ProjectItem,Skill
from accounts.models import User
from django.db.models import Q


class ResumeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/indexes/jobsapp/resume_text.txt')
    skills = indexes.MultiValueField()
    projects = indexes.MultiValueField()

    #author = indexes.CharField(model_attr='user')
    #pub_date = indexes.DateTimeField(model_attr='pub_date')
    
    def get_model(self):
        return Resume
    	
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    # def prepare_skills(self, obj):
    # 	return [o.category for o in obj.skills.all()]

    def prepare_skills(self, obj):
        skillset= Skill.objects.filter(id__in=obj.skills.only("skill"))
        return [o.name for o in skillset]

    # def prepare_projects(self, obj):
    # 	projects= Project.objects.filter( id__in=obj.projects.only("project"))
    # 	return [o.title for o in projects]

    def prepare(self, obj):
    	prepared_data = super(ResumeIndex, self).prepare(obj)
    	prepared_data['text'] += ' '.join(self.prepare_skills(obj))
    	#prepared_data['text'] += ' '.join(self.prepare_projects(obj))
    	return prepared_data

# class SkillItemIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/indexes/jobsapp/skillitem_text.txt')
#     #author = indexes.CharField(model_attr='user')
#     #pub_date = indexes.DateTimeField(model_attr='pub_date')
   
#     def get_model(self):
#         return SkillItem

#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

from accounts.managers import UserManager

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    username = None
    middle_name = models.CharField(max_length=15,blank=True)
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='user_images')

    def __str__(self):
        return f'{self.user.first_name} Profile'





def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
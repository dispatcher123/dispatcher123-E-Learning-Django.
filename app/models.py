from django.db import models
from django.utils.text import slugify
from account.models import CustomUser
# Create your models here.


SUBSCRIPTION=(
    ('F','FREES'),
    ('M','MONHTLY'),
    ('Y','YEARLY')
)

class Profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    is_pro=models.BooleanField(default=False)
    pro_expiry_date=models.DateTimeField(null=True,blank=True)
    subscription=models.CharField(max_length=100,default='FREE',choices=SUBSCRIPTION)


    def __str__(self):
        return self.user.email




class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        self.slug=slugify(self.name)
        super(Category,self).save(*args, **kwargs)


class Course(models.Model):
    title=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250)
    description=models.TextField()
    image=models.ImageField(upload_to='image')
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    category=models.ManyToManyField(Category,related_name='category')
    is_premium=models.BooleanField(default=False)
    video=models.FileField(upload_to='video', blank=False, max_length=500)



    def __str__(self):
        return self.title

    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.title)
        super(Course,self).save(*args, **kwargs)
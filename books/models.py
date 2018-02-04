from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)
    bio = models.TextField()
    picture = models.ImageField(upload_to='images/authors/') 

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name

class Book(models.Model):
    title = models.CharField(max_length=70)
    summary = models.TextField()
    date_of_publish = models.DateField()
    image = models.ImageField(upload_to='images/books/') 
    author = models.ManyToManyField(Author)
    user = models.ManyToManyField(User, through='UserBook')

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to='images/categories/') # will add upload to attribute later!
    book = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class UserBook(models.Model):
    STATUS = (
        ('wishlist', 'Add To Wishlist'),
        ('read', 'Read'),
        ('reading', 'Currently Reading'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    rate =  models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    comment = models.TextField()

    def __str__(self):
        return '{} {}'.format(user, book)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/users/')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.get_full_name()
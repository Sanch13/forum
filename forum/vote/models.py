from django.core.validators import RegexValidator
from django.db import models


class Project(models.Model):
    fio = models.CharField(max_length=300)
    phone = models.CharField(max_length=12,
                             validators=[RegexValidator(regex='^[0-9]*$',
                                                        message='Телефон должен состоять из цифр')])
    email = models.EmailField(unique=True)
    project_name = models.CharField(max_length=300)
    project_description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')


class Photo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/')

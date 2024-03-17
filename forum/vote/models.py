import os

from django.core.validators import RegexValidator
from django.db import models


class Project(models.Model):
    fio = models.CharField(max_length=300)
    code = models.CharField(max_length=3,
                            validators=[RegexValidator(regex='^[0-9]*$',
                                                       message='Код должен состоять из цифр')],
                            default='')
    phone = models.CharField(max_length=7,
                             validators=[RegexValidator(regex='^[0-9]*$',
                                                        message='Телефон должен состоять из цифр')])
    email = models.EmailField()
    project_name = models.CharField(max_length=300, unique=True)
    project_description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_file_upload_path(instance, filename):
    project_name = f"{instance.project.fio}-{instance.project.project_name}"
    return os.path.join('files', project_name, filename)


class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_upload_path)

    # def __repr__(self):
    #     return f"[ID: {self.project.id}] -> {self.file}"

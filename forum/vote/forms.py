from django import forms
from django.core.validators import RegexValidator
from captcha.fields import CaptchaField

from .models import Project, File


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["fio", "phone", "email", "project_name", "project_description"]


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateProjectForm(forms.Form):
    name = forms.CharField(max_length=300,
                           label="ФИО")
    code = forms.CharField(max_length=2,
                           validators=[RegexValidator(regex='^[0-9]*$',
                                                       message='Код должен состоять из цифр.')],
                           initial='')
    phone = forms.CharField(max_length=7,
                            validators=[RegexValidator(regex='^[-0-9]*$',
                                                       message='Телефон должен состоять из цифр.')],
                            label="Номер телефона",
                            initial='')
    email = forms.EmailField(label="Электронная почта")
    project_name = forms.CharField(max_length=200,
                                   label="Наименование проекта",
                                   widget=forms.TextInput(
                                       attrs={'placeholder': '200 символов'}))
    main_idea = forms.CharField(max_length=250,
                                label="Основная идея",
                                widget=forms.TextInput(
                                    attrs={'placeholder': '250 символов'})
                                )
    project_description = forms.CharField(widget=forms.Textarea,
                                          max_length=300,
                                          label="Описание проекта")
    files = MultipleFileField(label="Файлы проекта", required=False)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control'

from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


#название придумываем сами
# class AddPostForm(forms.Form):
# 	content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
# 	is_published = forms.BooleanField(label="Публикация", required=False, initial=True) # label нужен для нужного нам 
# 																						# 	отображения названия полей формы
# 																						# required=False - необязательное поле 
# 																						# initial=True - изначально делает поле помеченным

# Закомментировали, т.к. формы тесно связанные с моделями лучше связывать напрямую

class AddPostForm(forms.ModelForm):
	captcha = CaptchaField(label="Капча")
	class Meta:
		model = Riddle
		# fields = '__all__' #если речь идет о всех полях, кроме тех, которые заполняются автоматически
		fields = ['photo', 'content', 'answer', 'is_published']
		widgets = {
			'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
			'answer': forms.TextInput(attrs={'cols': 10, 'rows': 1}),
		} #индивидуальные стили для каждого поля

	#Делаем свой собственный вадидатор на одно поле. Начинается всегда с 'clean_', а потом нужное нам поле
	def clean_content(self):
		content = self.cleaned_data['content']
		if len(content) > 1000:
			raise ValidationError('Длина превышает 200 символов')
		return content

	# Валидатор на всю форму
	def clean(self):
		cleaned_data = super().clean()
		content = self.cleaned_data['content']
		photo = self.cleaned_data['photo']

		if photo == None and content == '':
			raise ValidationError('Добавьте или фотографию, или контент, или и то, и другое')
		return cleaned_data


# Форма регистрации
class RegisterUserForm(UserCreationForm):
	username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
	password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
		# Почему-то не работает
		# widgets = {
		# 	'username': forms.TextInput(attrs={'class': 'form-input'}), 
		# 	'password1': forms.PasswordInput(attrs={'class': 'form-input'}), 
		# 	'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
		# }


# Форма авторизации
class LoginUserForm(AuthenticationForm):
	username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
	password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddAnswer(forms.Form):
	answer = forms.CharField(widget=forms.TextInput(attrs={'cols': 10, 'rows': 1}), label="Ответ")

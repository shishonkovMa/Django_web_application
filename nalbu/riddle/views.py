from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm #стандартная форма регистрации
														 #закомментировали,т.к. прописали свой собственный класс регистрации в файл forms.py
# from django.contrib.auth.forms import AuthenticationForm # аналогично вышенаписанному
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from datetime import datetime
from .forms import *
from .models import *


menu = [{'title': "Нерешенные", 'url_name': 'unresolved'},
		{'title': "Решенные", 'url_name': 'solved'},
		{'title': "Добавить загадку", 'url_name': 'addriddle'}]
		# {'title': "Войти", 'url_name': 'login'}]


class RiddleHome(ListView):
	model = Riddle
	template_name = 'riddle/index.html' #html-страница для данного представления
	context_object_name = 'riddles'
	# extra_context = {'title': 'Главная страница'} #Можно передавать только статические/неизменяемые данные,
												  #т.е. списки передать нельзя. Для этого:
	def get_context_data(self, *, object_list=None, **kwargs): # создается специальная функция, которая затем предаются в 'riddle/index.html'
		context = super().get_context_data(**kwargs) #получаем динамический контекст, который уже сформирован для 'riddle/index.html'
													 #super() - обращаемся к базовому классу ListView. Далее берем из него уже существующий контекс
		context['menu'] = menu
		context['title'] = 'Главная страница'
		context['request_path'] = '/'
		return context

	def get_queryset(self): #с помощью данной функции мы можем указывать, что именно выбирать из модели
		return Riddle.objects.filter(is_published=True) #вернуть на главную страницу только те записи, для которых уснановлено тру

# def index(request):
# 	riddles = Riddle.objects.all()
# 	context = {'riddles': riddles,
# 			   'menu': menu,
# 			   'title': 'Главная страница',
# 			   'request_path': str(request.path)[1:-1]}
# 	return render(request, 'riddle/index.html', context=context)


def unresolved(request):
	riddles = Riddle.objects.filter(cat_id=1)
	context = {'riddles': riddles,
			   'menu': menu,
			   'title': 'Нерешенные',
			   'request_path': str(request.path)[1:-1]}
	return render(request, 'riddle/index.html', context=context)


def solved(request):
	riddles = Riddle.objects.filter(cat_id=2)
	context = {'riddles': riddles,
			   'menu': menu,
			   'title': 'Решенные',
			   'request_path': str(request.path)[1:-1]}
	return render(request, 'riddle/index.html', context=context)


# class ShowRiddle(DetailView):
# 	model = Riddle
# 	template_name = 'riddle/riddle.html'
# 	pk_url_kwarg = 'riddle_id'
# 	context_object_name = 'riddle'

# 	def get_context_data(self, *, object_list=None, **kwargs):
# 		context = super().get_context_data(**kwargs) 
													
# 		context['menu'] = menu
# 		context['title'] = context['riddle']
# 		context['request_path'] = ''
# 		return context

# def show_riddle(request, riddle_id):
# 	riddle = get_object_or_404(Riddle, pk=riddle_id)

# 	context = {'riddle': riddle,
# 			   'menu': menu,
# 			   'content': riddle.content,
# 			   'request_path': str(request.path)[1:-1]}
# 			   # 'request_path': str(request.META['HTTP_REFERER']).split('/')[-2]}
# 			   # Для того, чтобы запись в верхнем меню оставалась выделенной 
# 			   # при переходе на страницу загадки
# 	return render(request, 'riddle/riddle.html', context=context)


def show_riddle(request, riddle_id):
	riddle = get_object_or_404(Riddle, pk=riddle_id)
	if request.method == 'POST':
		form = AddAnswer(request.POST)
		if form.is_valid():
			# print(form.cleaned_data)
			if form.cleaned_data['answer'].lower() == riddle.answer:
				riddle.cat_id = 2
				riddle.save()
				return redirect('unresolved')
			else:
				form.add_error(None, 'Ответ не верен. Попробуйте еще.')
	else:
		form = AddAnswer()
	return render(request, 'riddle/riddle.html', {'riddle': riddle,
												   'form': form,
												   'menu': menu,
												   'request_path': str(request.path)[1:-1]})


class AddRiddle(LoginRequiredMixin, CreateView):
	form_class = AddPostForm
	template_name = 'riddle/addpage.html'
	success_url = reverse_lazy('home') #По дефолту сработает get_absolute_url, но при помощи данного фрагмента кода, перенаправление будет на домашнюю страницу
	login_url = reverse_lazy('login') #указвает адрес перенаправления для незарегистрированного пользователя
	# raise_exception = True # Если хотим, чтобы исключение обрабатывалось. В нашем случае 403 доступ запрещен

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs) 
													
		context['menu'] = menu
		context['title'] = 'Добавление загадки'
		context['request_path'] = 'addriddle'
		return context

# @login_required # декоратор вместо LoginRequiredMixin для класса представления (не забыть про его импорт)
# def addriddle(request):
# 	if request.method == 'POST':
# 		form = AddPostForm(request.POST, request.FILES) #второй аргумент - список файлов, которые были переданы на сервер из формы
# 		if form.is_valid(): # корректно ли заполнены данные и переданы на сервер
# 			try:
# 				# Riddle.objects.create(**form.cleaned_data) # если форма, не связана с моделью
# 				form.save() #если форма, связана с моделью
# 				return redirect('home')
# 			except:
# 				form.add_error(None, 'Ошибка добавлеия поста')
# 	else:
# 		form = AddPostForm()
# 	context = {'form': form,
# 			   'menu': menu,
# 			   'title': 'Добавление загадки',
# 			   'request_path': str(request.path)[1:-1]}
# 	return render(request, 'riddle/addpage.html', context=context)


class RegisterUser(CreateView):
	form_class = RegisterUserForm # из файла forms.py (для лучшего отображения формы), хотя могли бы использовать UserCreationForm прямо здесь
	template_name = 'riddle/register.html'
	success_url = reverse_lazy('login')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs) 
													
		context['menu'] = menu
		context['title'] = 'Регистрация'
		context['request_path'] = 'register'
		return context

	#Для того чтобы после регистрации пользователь был сразу авторизован
	def form_valid(self, form):
		user = form.save() #добавляем пользователя в базу данных
		login(self.request, user) #функция-авторизации джанго
		return redirect('home')

# def login(request):
# 	context = {'menu': menu,
# 			   'title': 'Войти',
# 			   'request_path': None}
# 	return render(request, 'riddle/base.html', context=context)


class LoginUser(LoginView):
	form_class = LoginUserForm # из файла forms.py (для лучшего отображения формы), хотя могли бы использовать AuthenticationForm
	template_name = 'riddle/login.html'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs) 
													
		context['menu'] = menu
		context['title'] = 'Авторизация'
		context['request_path'] = 'login'
		return context

	def get_success_url(self):
		return reverse_lazy('home')# или в settings проекта параметр LOGIN_REDIRECT_URL


def logout_user(request):
	logout(request) #джанговская функция логаут
	return redirect('home')

def pageNotFound(request, exception):
	return HttpResponseNotFound("<h1>Страница не найдена</h1>")

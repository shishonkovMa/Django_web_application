from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *



urlpatterns = [
	path('', RiddleHome.as_view(), name='home'), # Для класса-представления
	# path('', cache_page(60)(RiddleHome.as_view()), name='home'), # если хотим закешировать страницу на нужное количество секунд
	# path('', index, name='home'),
	path('unresolved/', unresolved, name='unresolved'),
	path('solved/', solved, name='solved'),
	path('addriddle/', AddRiddle.as_view(), name='addriddle'),
	# path('addriddle/', addriddle, name='addriddle'),
	path('register/', RegisterUser.as_view(), name='register'),
	# path('register/', login, name='register'),
	path('login/', LoginUser.as_view(), name='login'),
	# path('login/', login, name='login'),
	path('logout/', logout_user, name='logout'),
	# path('riddle/<int:riddle_id>/', ShowRiddle.as_view(), name='riddle'),
	path('riddle/<int:riddle_id>/', show_riddle, name='riddle'),
]	
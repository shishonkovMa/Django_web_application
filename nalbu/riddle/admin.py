from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


#Для дополнительных настроек админки регистрируется классы моделей
class RiddleAdmin(admin.ModelAdmin):
	#Могут быть и другие атрибуты, можно посмотреть в документации
	list_display = ('id', 'content', 'answer', 'get_html_photo', 'time_create', 'time_update', 'cat', 'is_published') #список полей, которые мы хотим видеть в админке
	list_display_links = ('id', 'content') #cписок полей-ссылок для перехода на страницу загадки
	search_fields = ('content', 'answer') #список полей, по которым можно осуществлять поиск
	list_editable = ('is_published', ) #список полей, которые редактируемы в админке в списке загадок
	list_filter = ('is_published', 'time_create') #поля, по которым можно фильтровать список загадок в админке
	
	fields = ('cat', 'content', 'answer', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update') #отображение полей в админке на странице загадки
	readonly_fields = ('time_create', 'time_update', 'get_html_photo') # нередактируемые поля, которые также заносятся в строку выше
	save_on_top = True #в админке будет показываться строка "удалить, сохранить и т.д"

	#название придумываем сами
	def get_html_photo(self, object):
		if object.photo:
			return mark_safe(f"<img src='{object.photo.url}' width=50>") #функция mark_safe указывает не экранировать теги, а выполнять их

	get_html_photo.short_description = "Миниатюра" #для админки


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_display_links = ('id', 'name')
	search_fields = ('name', )


#Для отображения модели в админке
admin.site.register(Riddle, RiddleAdmin) #1ым параметром модель, 2ым вспомогательный класс админки
admin.site.register(Category, CategoryAdmin)
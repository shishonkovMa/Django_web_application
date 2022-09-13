from django import template
from riddle.models import *
from datetime import datetime, timezone


register = template.Library() # регистрация собственных шаблонных тегов


@register.simple_tag()
def time_diff(time_create, time_update=None):
	def timedelta_to_dhms(duration):
	    days, seconds = duration.days, duration.seconds
	    hours = seconds // 3600
	    # minutes = (seconds % 3600) // 60
	    return days, hours
	
	if time_update:
		diff = time_update - time_create
		resp = 'Решено за'
	else:
		diff = datetime.now(timezone.utc) - time_create
		resp = ''
	d, h = timedelta_to_dhms(diff)
	d_t, h_t = int(float(d)), int(float(h))
	if d_t%10 == 1:
		d = str(f'{d} день')
	elif d_t%10 in [2, 3, 4]:
		d = str(f'{d} дня')
	elif d_t == 0:
		d = ''
	else:
		d = str(f'{d} дней')

	if h_t in [1, 21]:
		h = str(f'{h} час')
	elif h_t in [2, 3, 4, 22, 23]:
		h = str(f'{h} часа')
	else:
		h = str(f'{h} часов')

	return resp+'\n'+d+' '+h



# ### ПРОСТЫЕ ТЕГИ

# # Опишем функцию для работы тега
# @register.simple_tag(name='getcats') #Превращаем функцию в тег
# 									 #поле "name" нужно для обращения к тегу не по имени "get_categories",
# 									 #а по заданному нами значению
# 									 #если мы обозначаем "name", то "get_categories" перестает работать
# def get_categories(filter=None):
# 	if not filter:
# 		return Category.objects.all()
# 	else:
# 		return Category.objects.filter(pk=filter)
# # Для применения тега на html-странице мы пишем:
# # {% getcats as categories %}
# # Для применения тега с фильтром:
# # {% getcats filter=1 %} или {% getcats 1 %}





# ### ВКЛЮЧАЮЩИЕ ТЕГИ
# #позволяют фомировать свой собственный шаблон и возвращать фрагмент html-страницы

# @register.inclusion_tag('riddle/list_categories.html')
# def show_categories():
# 	cats = Category.objects.all()
# 	return {"cats": cats}

# #вызывается просто: {% show_categories %}
# #а в файле list_categories.html заменяется на "cats".




# # После примениния тегов, мы убираем соответствующие переменные из представлений 

# # Также на базовой html-странице прописываем {% load riddle_tags %}

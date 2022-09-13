from django.db import models
from django.urls import reverse


class Riddle(models.Model):
	content = models.TextField(null=True, blank=True, verbose_name="Текст загадки") #verbose_name для отображения в админке
	answer = models.CharField(max_length=40, blank=False, verbose_name="Ответ")
	photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
	time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
	time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
	is_published = models.BooleanField(default=True, verbose_name="Публикация")
	cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Категория", default=1)

	def __str__(self):
		return self.content #метод для отображения контента

	def get_absolute_url(self):
		return reverse('riddle', kwargs={'riddle_id': self.pk}) #используется в шаблоне, чтобы не использовать параметр "url"
																#также благодаря ему можно из админки смотреть, как выглядит страница на сайте
																#+ работает только с записями базы данных,т.е. в нашем случае не будет работать
																#	с элементами меню
																#в том числе не нужно менять шаблон, если мы захотим оформить не по "pk", а по "slug"

	#для админки
	class Meta:
		verbose_name = "Загадка"
		verbose_name_plural = "Загадки"
		ordering = ['time_create', 'content']


class Category(models.Model):
	name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"
		ordering = ['id']

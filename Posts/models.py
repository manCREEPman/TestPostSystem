from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    picture = models.ImageField(upload_to='Posts/static/Posts/images', verbose_name='Картинка')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

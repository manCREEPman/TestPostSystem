from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    picture = models.ImageField(upload_to='Tests/static/Tests/images', verbose_name='Картинка')
    max_points = models.IntegerField(null=True, verbose_name='Максимальный балл')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestTask(models.Model):
    
    CHECK_TASK_CHOICES = [
        ('TE', 'Вручную'),
        ('CO', 'Автоматически')
    ]

    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    type = models.CharField(max_length=20, choices=CHECK_TASK_CHOICES, default='comp', verbose_name='Тип ответа')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    task_statement = models.TextField(verbose_name='Формулировка задания')
    correct_answer = models.TextField(verbose_name='Правильный ответ')
    points = models.IntegerField(verbose_name='Баллы')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class UserTest(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    result_points = models.IntegerField(verbose_name='Результирующий балл')
    check_status = models.BooleanField(verbose_name='Статус проверки')
    
    class Meta:
        verbose_name = 'Тест пользователя'
        verbose_name_plural = 'Тесты пользователя'

    
class UserTestTask(models.Model):
    CHECK_TASK_CHOICES = [
        ('TE', 'Вручную'),
        ('CO', 'Автоматически')
    ]

    user_test_id = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=CHECK_TASK_CHOICES, verbose_name='Тип ответа')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    task_statement = models.TextField(verbose_name='Формулировка задания')
    points = models.IntegerField(verbose_name='Баллы задания')
    correct_answer = models.TextField(verbose_name='Правильный ответ')
    user_answer = models.TextField(verbose_name='Ответ пользователя')
    user_file = models.FileField(upload_to='Tests/static/Tests/user_files',verbose_name='Файл ответа')
    user_points = models.IntegerField(default=0, verbose_name='Полученные баллы')
    check_status = models.BooleanField(verbose_name='Статус проверки')
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задание пользователя'
        verbose_name_plural = 'Задания пользователя'

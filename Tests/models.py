from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestTask(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    type = models.CharField(max_length=20, verbose_name='Тип ответа')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    task_statement = models.TextField(verbose_name='Формулировка задания')
    points = models.IntegerField(verbose_name='Баллы')

    def __unicode__(self):
        return this.title

    def __str__(self):
        return this.title

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
    

class CustomUser(models.Model):
    nickname = models.CharField(max_length=100, verbose_name='Логин')

    def __unicode__(self):
        return self.nickname

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name = 'Пользователи'


class UserTest(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    result_points = models.IntegerField(verbose_name='Результирующий балл')
    check_status = models.BooleanField(verbose_name='Статус проверки')
    
    class Meta:
        verbose_name = 'Тест пользователя'
        verbose_name = 'Тесты пользователя'

    
class UserTestTask(models.Model):
    user_test_id = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, verbose_name='Тип ответа')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    task_statement = models.TextField(verbose_name='Формулировка задания')
    points = models.IntegerField(verbose_name='Баллы задания')
    user_points = models.IntegerField(verbose_name='Полученные баллы')
    check_status = models.BooleanField(verbose_name='Статус проверки')
    
    def __unicode__(self):
        return this.title

    def __str__(self):
        return this.title

    class Meta:
        verbose_name = 'Задание пользователя'
        verbose_name_plural = 'Задания пользователя'
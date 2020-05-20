from django.db import models


class Planet(models.Model):
    """Планета"""
    name = models.CharField('Наименование', max_length=150, unique=True)

    def __str__(self):
        return self.name


class Sith(models.Model):
    """Ситх"""
    name = models.CharField('Имя', max_length=100)
    planet = models.ForeignKey(
        Planet,
        verbose_name='Планета',
        on_delete=models.CASCADE,
        related_name='siths',
    )

    def __str__(self):
        return self.name


class Recruit(models.Model):
    """Рекрут"""
    name = models.CharField('Имя', max_length=150)
    planet = models.ForeignKey(
        Planet,
        verbose_name='Планета',
        on_delete=models.CASCADE,
        related_name='recruits',
    )
    old = models.IntegerField('Возраст')
    email = models.EmailField('Почта')
    hand_shadow = models.ForeignKey(
        Sith,
        verbose_name='Рука тени',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='disciples',
        default=None
    )
    reviewed = models.BooleanField('Отбор', default=False)

    def __str__(self):
        return self.name


class Question(models.Model):
    """Вопрос"""
    question = models.TextField('Текст вопроса')
    active = models.BooleanField("Задавать ли", default=True)

    def __str__(self):
        return self.question


class ResultTest(models.Model):
    """Результат испытания"""
    recruit = models.ForeignKey(
        Recruit,
        verbose_name='Рекрут',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    answer = models.BooleanField('Ответ')

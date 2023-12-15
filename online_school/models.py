from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(_("название курса"), max_length=50)
    preview_img = models.ImageField(_("превью (картинка)"), upload_to='course/', **NULLABLE)
    description = models.TextField(_("описание курса"), **NULLABLE)
    
    payment = GenericRelation('Payment', related_query_name='course')
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
    
    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=_("курс"), on_delete=models.CASCADE)
    name = models.CharField(_("название урока"), max_length=50)
    description = models.TextField(_("описание урока"), **NULLABLE)
    preview_img = models.ImageField(_("превью (картинка)"), upload_to='lesson/', **NULLABLE)
    video_link = models.CharField(_("ссылка на видео"), max_length=250)
    
    payment = GenericRelation('Payment', related_query_name='lesson')
    
    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.course.name}: {self.name}'


PAYMENT_TYPE_CHOICES = (('cash', 'наличные'),
                ('card', 'карта'),)
class Payment(models.Model):
    user = models.ForeignKey(User, verbose_name=_("пользователь"), on_delete=models.CASCADE)
    date = models.DateField(_("дата оплаты"), auto_now=False, auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    purchased_item = GenericForeignKey('content_type', 'object_id')
    
    summ = models.IntegerField(_("сумма оплаты"))
    payment_type = models.CharField(_("способ оплаты"), choices=PAYMENT_TYPE_CHOICES, max_length=4)

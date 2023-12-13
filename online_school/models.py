from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(_("название курса"), max_length=50)
    preview_img = models.ImageField(_("превью (картинка)"), upload_to='course/', **NULLABLE)
    description = models.TextField(_("описание курса"), **NULLABLE)
    
    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(_("название урока"), max_length=50)
    description = models.TextField(_("описание урока"), **NULLABLE)
    preview_img = models.ImageField(_("превью (картинка)"), upload_to='lesson/', **NULLABLE)
    video_link = models.CharField(_("ссылка на видео"), max_length=250)
    
    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
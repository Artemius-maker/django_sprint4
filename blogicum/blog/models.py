from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseModel


# Create your models here.
User = get_user_model()


class Category(BaseModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(unique=True, verbose_name="Идентификатор",
                            help_text="Идентификатор страницы для URL; "
                            + "разрешены символы латиницы, "
                            + "цифры, дефис и подчёркивание.")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ['title']

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(verbose_name="Дата и время публикации",
                                    help_text="Если установить дату и время "
                                    + "в будущем — можно делать "
                                    + "отложенные публикации.")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор публикации",
        related_name='author')
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Местоположение",
        related_name='location')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, verbose_name="Категория", related_name='category')
    image = models.ImageField(
        verbose_name="Фото", upload_to='images/', blank=True)

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Текст поздравления')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ('created_at',)

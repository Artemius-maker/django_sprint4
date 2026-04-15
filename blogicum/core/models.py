from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено")
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.")

    class Meta:
        abstract = True

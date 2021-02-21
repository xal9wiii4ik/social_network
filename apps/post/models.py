import os

from django.contrib.auth import get_user_model
from django.db import models


def updating_image_name(title: str, image_name: str, username: str) -> os:
    """Func for updating image name"""

    image_extension = image_name.split(',')[-1]
    return os.path.join(f'{title}_{username}.{image_extension}')


def post_upload_path(obj: models.Model, filename: str) -> os:
    """Func for editing upload path"""

    return os.path.join(f'{obj.subject.subject}', filename)


class Subject(models.Model):
    """Model subject"""

    subject = models.CharField(max_length=99, verbose_name='Тема', unique=True)

    def __str__(self):
        return f'{self.pk}, subject: {self.subject}'

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Post(models.Model):
    """Model post"""

    owner = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True, related_name='post_owner')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, related_name='post_subject')
    title = models.CharField(max_length=30, verbose_name='Заглавие')
    body = models.TextField(max_length=1024, verbose_name='Тело поста')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(verbose_name='Фотография', null=True, blank=True, upload_to=post_upload_path)

    def __str__(self):
        return f'{self.pk}, {self.owner}, subject: {self.subject}, title: {self.title}'

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = updating_image_name(
                title=self.title,
                image_name=self.image.name,
                username=self.owner.username)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    """Model of comments"""

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        related_name='comment_owner',
        null=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comment_post')
    parent = models.ForeignKey(
        to='self',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comment_parents')
    text = models.TextField(verbose_name='Текст комментария')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f'{self.post.title}, {self.user.id}, {self.pk}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

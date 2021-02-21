from django.contrib.auth import get_user_model
from django.db import models


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

    def __str__(self):
        return f'{self.pk}, {self.owner}, subject: {self.subject}, title: {self.title}'

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

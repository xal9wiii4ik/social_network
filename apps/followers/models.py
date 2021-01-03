from django.contrib.auth import get_user_model
from django.db import models


class Follower(models.Model):
    """Model follower"""

    owner = models.ForeignKey(to=get_user_model(), related_name='owner', on_delete=models.CASCADE)
    follower = models.ForeignKey(to=get_user_model(), related_name='follower', on_delete=models.CASCADE)
    # TODO: OneToOne for follower

    def __str__(self):
        return f'{self.pk}, owner: {self.owner}, follower: {self.follower}'

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

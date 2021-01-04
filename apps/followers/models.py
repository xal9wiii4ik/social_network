from django.contrib.auth import get_user_model
from django.db import models


class Follower(models.Model):
    """Model follower"""

    owner = models.ForeignKey(to=get_user_model(), related_name='owner', on_delete=models.CASCADE)
    follower = models.ForeignKey(to=get_user_model(), related_name='follower', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}, owner: {self.owner}, follower: {self.follower}, ' \
               f's: {Follower.objects.filter(owner=self.owner).count()}'

    def save(self, *args, **kwargs):
        user = get_user_model().objects.get(id=self.owner.id)
        user.followers += 1
        user.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = get_user_model().objects.get(id=self.owner.id)
        user.followers -= 1
        user.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

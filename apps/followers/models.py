from django.contrib.auth import get_user_model
from django.db import models


class Follower(models.Model):
    """Model follower"""

    owner = models.ForeignKey(to=get_user_model(), related_name='follower_owner', on_delete=models.CASCADE)
    follower = models.ForeignKey(to=get_user_model(), related_name='follower', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}, owner: {self.owner}, follower: {self.follower}'

    def save(self, *args, **kwargs):
        user = get_user_model().objects.get(id=self.owner.id)
        user.followers += 1
        user.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = get_user_model().objects.get(id=self.owner.id)
        user.followers -= 1
        user.save()
        super(Follower, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class Subscriber(models.Model):
    """Model subscriber"""

    owner = models.ForeignKey(to=get_user_model(), related_name='subscriber_owner', on_delete=models.CASCADE)
    subscriber = models.ForeignKey(to=get_user_model(), related_name='subscriber', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}, owner: {self.owner}, follower: {self.subscriber}'

    def save(self, *args, **kwargs):
        user = get_user_model().objects.get(id=self.owner.id)
        user.subscribers += 1
        user.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = get_user_model().objects.get(id=self.owner.id)
        user.subscribers -= 1
        user.save()
        return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'



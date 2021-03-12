from django.contrib.auth import get_user_model
from django.db import models


class Follower(models.Model):
    """Model follower"""

    owner = models.ForeignKey(to=get_user_model(), related_name='follower_owner', on_delete=models.CASCADE, blank=True)
    follower = models.ForeignKey(to=get_user_model(), related_name='follower', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}, owner: {self.owner}, follower: {self.follower}'

    def save(self, *args, **kwargs):
        user_owner = get_user_model().objects.get(id=self.owner.id)
        user_owner.followers += 1
        user_follower = get_user_model().objects.get(id=self.follower.id)
        user_follower.subscribers += 1
        user_owner.save()
        user_follower.save()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user_owner = get_user_model().objects.get(id=self.owner.id)
        user_owner.followers -= 1
        user_follower = get_user_model().objects.get(id=self.follower.id)
        user_follower.subscribers -= 1
        user_owner.save()
        user_follower.save()
        return super(Follower, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

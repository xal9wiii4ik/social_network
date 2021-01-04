from django.contrib import admin
from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.userprofile.views import (
    AbstractUserGuestsViewSet,
    AbstractUserOwnerViewSet
)
from apps.followers.views import (
    FollowerModelViewSet,
    SubscriberModelViewSet,
)

router = SimpleRouter()
router.register(r'user_profile', AbstractUserOwnerViewSet)
router.register(r'guest_user_profile', AbstractUserGuestsViewSet)
router.register(r'followers', FollowerModelViewSet)
router.register(r'subscribers', SubscriberModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls

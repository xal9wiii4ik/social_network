from django.conf.urls import url
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
from apps.post.views import (
    SubjectModelViewSet,
    PostModelViewSet
)
from apps.auth_user.views import (
    RegistrationView,
    ActivationView
)

router = SimpleRouter()
router.register(r'user_profile', AbstractUserOwnerViewSet)
router.register(r'guest_user_profile', AbstractUserGuestsViewSet)
router.register(r'followers', FollowerModelViewSet)
router.register(r'subscribers', SubscriberModelViewSet)
router.register(r'posts', PostModelViewSet)
router.register(r'subjects', SubjectModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    url('auth/registration/', RegistrationView.as_view(), name='registration'),
    path('auth/activation/<str:uid>/<str:token>/', ActivationView.as_view(), name='activation')
]

urlpatterns += router.urls

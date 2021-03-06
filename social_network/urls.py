from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.userprofile.views import (
    AbstractUserGuestsViewSet,
    AbstractUserOwnerViewSet
)
from apps.followers.views import (
    FollowerModelViewSet,
)
from apps.post.views import (
    SubjectModelViewSet,
    PostModelViewSet,
    CommentModelViewSet,
    LikeDislikeApiView,
)
from apps.auth_user.views import (
    RegistrationView,
    ActivationView,
    LogInView,
    ResetPasswordView,
    SetNewPasswordView,
)
from social_network import settings

router = SimpleRouter()
router.register(r'user_profile', AbstractUserOwnerViewSet)
router.register(r'guest_user_profile', AbstractUserGuestsViewSet, basename='guestcustomuser')
router.register(r'followers', FollowerModelViewSet)
router.register(r'posts', PostModelViewSet)
router.register(r'subjects', SubjectModelViewSet)
router.register(r'comments', CommentModelViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/token/', TokenObtainPairView.as_view(), name='token'),

    path('auth/registration/', RegistrationView.as_view(), name='registration'),
    path('auth/activation/<str:uid>/<str:token>/', ActivationView.as_view(), name='activation'),
    path('auth/login/', LogInView.as_view(), name='login'),
    path('auth/reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth/reset_password/<str:uid>/<str:token>/', SetNewPasswordView.as_view(), name='reset_password_confirm'),

    path('likedislike/<str:post_pk>/', LikeDislikeApiView.as_view(), name='post_likes_dislikes'),
]

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

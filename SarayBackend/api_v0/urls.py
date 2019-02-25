from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'locations', LocationsViewSet)
router.register(r'photographs', PhotographsViewSet)
router.register(r'booking/types', BookingTypesViewSet)
router.register(r'booking/options', BookingOptionsViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
]
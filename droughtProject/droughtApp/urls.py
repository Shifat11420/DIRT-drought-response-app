from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'user', views.userInfo)
router.register(r'fields', views.userfield)
router.register(r'irrigation', views.irrigationActivity)

router.register(r'croptypes', views.CropTypes)
router.register(r'soiltypes', views.SoilTypes)
router.register(r'hydrologicgroups', views.hydrologicGroups)
router.register(r'drainageType', views.drainageTypeViewSet)
router.register(r'soilMoisture', views.soilMoistureViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CalculateDroughtAPIView',
         views.CalculateDroughtAPIView.as_view(), name='calcdroughtapi')
]

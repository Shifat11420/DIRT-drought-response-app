from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'croptypes', views.CropTypes)
router.register(r'soiltypes', views.SoilTypes)
router.register(r'hydrologicgroups', views.hydrologicGroups)
router.register(r'user', views.userInfo)
router.register(r'fields', views.userfield)
router.register(r'irrigation', views.irrigationActivity)


router.register(r'soilMoisture', views.soilMoistureViewSet)
# router.register(r'CropType1', views.CropType1ViewSet)
router.register(r'cropPeriod', views.cropPeriodViewSet)
router.register(r'drainageType', views.drainageTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CalculateDroughtAPIView',
         views.CalculateDroughtAPIView.as_view(), name='calcdroughtapi'),
    path('CropTypes2', views.CropTypes2.as_view(), name='croptypes2'),
    path('SoilTypes2', views.SoilTypes2.as_view(), name='soiltypes2'),
    path('HydrologicGroups2', views.hydrologicGroups2.as_view(),
         name='hydrologicgroups2'),
    path('User2', views.userInfo2.as_view(),
         name='user2'),
    path('Fields2', views.userfield2.as_view(),
         name='field2'),
    path('Irrigation2', views.irrigationActivity2.as_view(),
         name='irrigation2'),
]

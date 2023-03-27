from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'testdatamodel', views.testmodelViewSet)
router.register(r'croptypes', views.CropTypes)
router.register(r'soiltypes', views.SoilTypes)
router.register(r'hydrologicgroups', views.hydrologicGroups)
#
# router.register(r'croptype', views.CropType)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CalculateDroughtAPIView',
         views.CalculateDroughtAPIView.as_view(), name='calcdroughtapi'),
    path('CropTypes2', views.CropTypes2.as_view(), name='croptypes2'),
    path('SoilTypes2', views.SoilTypes2.as_view(), name='soiltypes2'),
    path('HydrologicGroups2', views.hydrologicGroups2.as_view(),
         name='hydrologicgroups2'),
    #
    #     path('CropType2', views.CropType2.as_view(), name='croptype2'),
]

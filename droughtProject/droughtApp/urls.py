from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'croptypes', views.CropTypes)
router.register(r'soiltypes', views.SoilTypes)
router.register(r'hydrologicgroups', views.hydrologicGroups)
router.register(r'user', views.user)
router.register(r'field', views.field)
router.register(r'irrigation', views.irrigation)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CalculateDroughtAPIView',
         views.CalculateDroughtAPIView.as_view(), name='calcdroughtapi'),
    path('CropTypes2', views.CropTypes2.as_view(), name='croptypes2'),
    path('SoilTypes2', views.SoilTypes2.as_view(), name='soiltypes2'),
    path('HydrologicGroups2', views.hydrologicGroups2.as_view(),
         name='hydrologicgroups2'),
    path('user2', views.user2.as_view(),
         name='user2'),
    path('field2', views.field2.as_view(),
         name='field2'),
    path('irrigation2', views.irrigation2.as_view(),
         name='irrigation2'),
]

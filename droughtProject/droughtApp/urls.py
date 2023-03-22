from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'testdatamodel', views.testmodelViewSet)
router.register(r'croptypes', views.CropTypes)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('CalculateDroughtAPIView',
         views.CalculateDroughtAPIView.as_view(), name='calcdroughtapi'),
    path('CropTypes2', views.CropTypes2.as_view(), name='croptypes2')
]

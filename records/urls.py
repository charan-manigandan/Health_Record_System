from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'health-records', views.HealthRecordViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('record/<int:pk>/', views.record_detail, name='record_detail'),
    path('records/', views.view_records, name='view_records'),
    path('upload/', views.upload_file, name='upload_file'),
    path('retrieve/<str:cid>/', views.retrieve_file, name='retrieve_file'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
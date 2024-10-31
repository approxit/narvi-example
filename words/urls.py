from rest_framework.routers import DefaultRouter

from words import views


router = DefaultRouter()
router.register(r'folders', views.FolderViewSet, basename='folder')
router.register(r'words', views.WordViewSet, basename='word')

urlpatterns = router.urls

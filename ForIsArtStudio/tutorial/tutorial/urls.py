from django.urls import include, path
from rest_framework import routers
from .quickstart import views
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'projects', views.ProjectViewSet,basename=views.ProjectViewSet)
router.register(r'check-lists', views.CheckListViewSet)
# router.register(r'mq', views.ShowDependViewSet, basename=views.CheckListViewSet)
# router.register(r'project', views.ShowProjectForMA, basename=views.ProjectViewSet)
# router.register(r'check-list', views.ShowCheckListForMA, basename=views.UserViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

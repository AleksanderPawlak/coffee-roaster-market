from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register("users", views.ApiUsersView)

urlpatterns = router.urls

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("", include("coffee_roaster_market.apps.coffee.urls", namespace="coffee")),
    path("item", include("coffee_roaster_market.apps.item.urls", namespace="item")),
    path("admin/", admin.site.urls),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/account/", include("coffee_roaster_market.apps.account.urls")),
]

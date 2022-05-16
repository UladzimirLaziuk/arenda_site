from django.contrib import admin
from django.urls import path, include
from site_app.models import Renter
from site_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', views.RenterAdViewList.as_view(), name='renter_ads_list'),
    path('create', views.RenterViewCreate.as_view(), name='renter_create'),
    path('search', views.RenterViewSearch.as_view(), name='renter_search'),
    path('update/<int:pk>', views.RenterUpdateView.as_view(), name='renter_update'),
    path('delete/<int:pk>', views.RenterDeleteView.as_view(), name='renter_delete'),
    path('ad_detail/<int:pk>', views.RenterDetailView.as_view(), name='renterad_detail'),
    # 'ads/<int:pk>/edit/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

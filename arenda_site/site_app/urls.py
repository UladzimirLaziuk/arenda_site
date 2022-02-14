from django.contrib import admin
from django.urls import path
from site_app.models import Renter
from site_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RenterViewList.as_view(), name='renter_list'),
    path('create', views.RenterViewCreate.as_view(), name='renter_create'),
    path('search', views.RenterViewSearch.as_view(), name='renter_search'),
    path('update/<int:pk>', views.RenterUpdateView.as_view(), name='renter_update'),
    path('delete/<int:pk>', views.RenterDeleteView.as_view(), name='renter_delete'),
    path('detail/<int:pk>', views.RenterDetailView.as_view(), name='renter_detail'),
    # 'ads/<int:pk>/edit/
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

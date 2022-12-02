from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('upload', views.upload, name="upload"),
    path('get_table_data', views.get_table_data, name="get_table_data"),
    path('get_bar_chart', views.get_bar_chart, name="get_bar_chart"),
    path('get_data_filters', views.get_data_filters, name="get_data_filters"),
    path('check_cache', views.check_cache, name="check_cache"),
    path('clear_chart', views.clear_chart, name="clear_chart"),
    path('get_line_chart', views.clear_chart, name="get_line_chart"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
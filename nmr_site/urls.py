from django.contrib import admin
from django.urls import path
from chemistry.views import predict_compound, export_pdf, history_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', predict_compound, name='predict'),
    path('history/', history_list, name='history_list'),
    # Use the ID instead of the name for a unique, URL-safe reference
    path('export/<int:test_id>/', export_pdf, name='export_pdf'),
]
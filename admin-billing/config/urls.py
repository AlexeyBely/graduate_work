from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin-billing/', admin.site.urls),
]


admin.site.site_header = 'Администрирование оплаты' 
admin.site.index_title = 'Администрирование оплаты'               
admin.site.site_title = 'Администрирование оплаты' 

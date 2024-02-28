from django.contrib import admin
from django.urls import path, include

"""
Change admin panel site_header,site_title, index_title
"""
admin.site.site_header = "ShoppinglyX Site Administration "
admin.site.site_title = "ShoppinglyX Site Administration "
admin.site.index_title = "Welcome To ShoppinglyX Site Administration"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]

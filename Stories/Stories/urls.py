from django.contrib import admin
from django.urls import path, include

######## this is the project 'urls.py' file ###########
#####    . is to indicate the current directory, 'views.py' file from the current directory
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('account/', include( 'app_login.urls' )),
    path('blog/', include( 'app_blog.urls' )),
]

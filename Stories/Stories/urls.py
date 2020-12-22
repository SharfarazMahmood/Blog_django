from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

######## this is the project 'urls.py' file ###########
#####    . is to indicate the current directory, 'views.py' file from the current directory
from . import views

######## imports form image viewing
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('account/', include( 'app_login.urls' )),
    path('blog/', include( 'app_blog.urls' )),

]
##### urls for image/static files
# if settings.DEBUG :
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""myreader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from ic_shop.api.v1 import apiViews as touchViews
from django.urls import path

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', touchViews.index),
    url(r'^add/(\d+)/(\d+)/$', touchViews.add, name='add'),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls),
    # url(r'^ueditor/', include('DjangoUeditor.urls')),
    # url(r'^progressbarupload/', include('progressbarupload.urls')),
    # api version 1.0
    url(r'^v1/', include('ic_shop.api.v1.urls')),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




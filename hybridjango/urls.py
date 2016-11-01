"""hybridjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from apps.events.views import EventList, updatek

urlpatterns = [
                  url(r'^$', EventList.as_view(template_name='frontpage.html'), name='home'),
                  url(r'^admin/', admin.site.urls),
                  url(r'^kilt/', include('apps.kiltshop.urls'), name='kiltshop'),
                  url(r'^bedkom/', include('apps.bedkom.urls')),
                  url(r'^hybrid/', include('apps.registration.urls'), name='accounts'),
                  url(r'^quiz/', include('apps.quiz.urls')),
                  url(r'^arrangementer/', include('apps.events.urls'), name='events'),
                  url(r'^avstemning/', include('apps.ballot.urls'), name='ballot'),

                  # Static pages, only temporary (short on time before genfors)
                  url(r'^strikk/', TemplateView.as_view(template_name='staticpages/hybridastrikk.html')),
                  url(r'^statutter/', TemplateView.as_view(template_name='staticpages/statutter.html')),
                  url(r'^griffens_orden/', TemplateView.as_view(template_name='staticpages/griffens_orden.html')),
                  url(r'^om_hybrida/', TemplateView.as_view(template_name='staticpages/about.html'), name='about'),
                  url(r'^for_bedrifter/', TemplateView.as_view(template_name='staticpages/for_companies.html'),
                      name='for_companies'),
                  url(r'^updatek/', updatek, name='updatek'),
                  url(r'^komite/', TemplateView.as_view(template_name='staticpages/committees.html'), name='committees'),
                  url(r'^kontakt_oss/', TemplateView.as_view(template_name='staticpages/contact_us.html'), name='contact_us'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

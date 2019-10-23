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
from django.views.generic import RedirectView

from apps.staticpages.views import FrontPage

urlpatterns = [
                  url(r'^$', FrontPage.as_view(template_name='frontpage.html'), name='home'),
                  url(r'^admin/', admin.site.urls),

                  url(r'^evaluation/', include('apps.evaluation.urls')),
                  url(r'^kilt/', include('apps.kiltshop.urls', namespace='kilt'), name='kiltshop'),
                  url(r'^bedkom/', include('apps.bedkom.urls')),
                  url(r'^kalender/', include('apps.eventcalendar.urls'), name='calendar'),
                  url(r'^hybrid/', include('apps.registration.urls'), name='accounts'),
                  url(r'^quiz/', include('apps.quiz.urls')),
                  url(r'^hendelser/', include('apps.events.urls'), name='events'),
                  url(r'^avstemning/', include('apps.ballot.urls'), name='ballot'),
                  url(r'^stillingsutlysninger/', include('apps.jobannouncements.urls', namespace='jobs'),
                      name='announcements'),
                  url(r'', include('apps.staticpages.urls')),
                  url(r'^griffensorden/', include('apps.griffensorden.urls'), name='griffensorden'),
                  url(r'^search/', include('apps.search.urls'), name='search'),
                  url(r'^rfid/', include('apps.rfid.urls'), name='rfid'),
                  url(r'^gitlab/', include('apps.gitlab.urls'), name='gitlab'),
                  url(r'^achievements/', include('apps.achievements.urls'), name='achievements'),

                  url(r'^api/', include('apps.api.urls'), name='api'),
                  url(r'^tinymce/', include('tinymce.urls')),
                  url(r'^vevkom/', include('apps.vevkom.urls'), name='vevkom'),
                  url(r'^hybridopedia/', include('apps.hybridopedia.urls'), name='hybridopedia'),
                  url(r'interestgroups', include('apps.interestgroups.urls'), name='interestgroups'),
                  # url(r'^butikk/', include('apps.merchandise.urls'), name='merchandise')

                  # TODO temprary, remove after 32. general assembly  2019-03-27
                  url(r'^hjelp$', RedirectView.as_view(url='https://forms.gle/jcr8hjdvP8tJKzGL6'), name='missing-user')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

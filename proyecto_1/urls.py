from django.conf.urls import patterns, include, url

from django.contrib import admin



admin.autodiscover()


  
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto_1.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
 
    url(r'^',include('citas.urls', namespace='citas')),
    url(r'^admin/', include(admin.site.urls)),
	#url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    #url(r'', 'citas.views.index'),
)



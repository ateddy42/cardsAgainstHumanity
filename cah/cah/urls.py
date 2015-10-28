from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^admin/', include(admin.site.urls)),

# cah
    url(r'^accounts/login/$', 'cah.views.login'),
    url(r'^accounts/logout/$', 'cah.views.logout'),
    url(r'^accounts/pwd/$', 'cah.views.pwd'),
    url(r'^robots.txt$', 'cah.views.robots'),

#game
    url(r'^$', 'game.views.home'),
    url(r'^judge/$', 'game.views.judge'),
    url(r'^play/$', 'game.views.play'),
    url(r'^leaders/$', 'game.views.leaders'),
    url(r'^genHands/$', 'game.views.genHands'),
    url(r'^addCards/$', 'game.views.addCards'),
)

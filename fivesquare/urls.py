from django.conf.urls import patterns, include, url
from api import views
from accounts.views import login_view
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login_view),
    url(r'^api/business/$', views.BusinessList.as_view()),
    url(r'^api/business/(?P<id>[\w]{24})/$', views.BusinessDetails.as_view()),
    url(r'^api/business/(?P<id>[\w]{24})/reviews/$',
        views.BusinessReviewList.as_view()),
)
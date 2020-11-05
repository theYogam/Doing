from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test, permission_required, login_required
from ikwen_webnode.webnode.views import FlatPageView

from doing.views import Home
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Doing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^laakam/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^currencies/', include('currencies.urls')),

    url(r'^kakocase/', include('ikwen_kakocase.kakocase.urls', namespace='kakocase')),
    url(r'^kako/', include('ikwen_kakocase.kako.urls', namespace='kako')),
    url(r'^trade/', include('ikwen_kakocase.trade.urls', namespace='trade')),
    url(r'^billing/', include('ikwen.billing.urls', namespace='billing')),
    url(r'^rewarding/', include('ikwen.rewarding.urls', namespace='rewarding')),
    url(r'^revival/', include('ikwen.revival.urls', namespace='revival')),
    url(r'^marketing/', include('ikwen_kakocase.commarketing.urls', namespace='marketing')),
    url(r'^sales/', include('ikwen_kakocase.sales.urls', namespace='sales')),
    url(r'^cashout/', include('ikwen.cashout.urls', namespace='cashout')),
    url(r'^theming/', include('ikwen.theming.urls', namespace='theming')),

    url(r'^page/(?P<url>[-\w]+)/$', FlatPageView.as_view(), name='flatpage'),
    url(r'^blog/', include('ikwen_webnode.blog.urls', namespace='blog')),
    url(r'^web/', include('ikwen_webnode.web.urls', namespace='web')),
    url(r'^items/', include('ikwen_webnode.items.urls', namespace='items')),
    url(r'^echo/', include('echo.urls', namespace='echo')),

    url(r'^reporting/', include('ikwen_foulassi.reporting.urls', namespace='reporting')),
    url(r'^school/', include('ikwen_foulassi.school.urls', namespace='school')),
    url(r'^foulassi/', include('ikwen_foulassi.foulassi.urls', namespace='foulassi')),

    url(r'^echo/', include('echo.urls', namespace='echo')),
    url(r'^daraja/', include('daraja.urls', namespace='daraja')),

    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),
    url(r'^home/$', login_required(Home.as_view()), name='home'),
    url(r'^', include('doing.urls', namespace='doing')),

)

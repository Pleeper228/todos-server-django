from django.conf.urls import url
from . import views

app_name = 'todos'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<list_task_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<list_task_id>[0-9]+)/$', views.asss, name='asss'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<list_task_id>[0-9]+)/completing/$', views.completing, name='completing'),
    url(r'^(?P<list_task_id>[0-9]+)/json/$', views.detail_json, name='detail_json'),
    url(r'^json/$', views.list_json, name='list_json'),
    url(r'^create_task_json/$', views.create_task_json, name='create_task_json'),
    url(r'^(?P<list_task_id>[0-9]+)/item/(?P<list_item_id>[0-9]+)/completed/$', views.item_completed, name='item_completed'),
    url(r'^(?P<list_task_id>[0-9]+)/create_item/$', views.create_item, name='create_item'),
]

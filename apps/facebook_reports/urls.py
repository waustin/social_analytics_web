from django.conf.urls import url
from django.views.generic import TemplateView
from .views import FacebookPostReportView, FacebookPageReportView, FacebookGraphAPIReport
# Create your app urls here

urlpatterns = [
    # Example
    url(r'^post-report/$',
        FacebookPostReportView.as_view(),
        name='facebook_post_report'),

    url(r'^page-report/$',
        FacebookPageReportView.as_view(),
        name='facebook_page_report'),

    # Graph API Reports
    url(r'^graph/page-report/$',
        FacebookGraphAPIReport.as_view(),
        name='facebook_graph_api_report'),
]

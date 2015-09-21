from django.conf.urls import url
from .views import FacebookPostReportView, FacebookPageReportView
# Create your app urls here

urlpatterns = [
    # Example
    url(r'^post-report/$',
        FacebookPostReportView.as_view(),
        name='facebook_post_report'),

    url(r'^page-report/$',
        FacebookPageReportView.as_view(),
        name='facebook_page_report')
]

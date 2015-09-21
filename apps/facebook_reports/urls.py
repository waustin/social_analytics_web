from django.conf.urls import url
from .views import FacebookPostReportView
# Create your app urls here

urlpatterns = [
    # Example
    url(r'^post-report/$',
        FacebookPostReportView.as_view(),
        name='facebook_post_report')
]

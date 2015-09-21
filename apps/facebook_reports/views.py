from django.views.generic import View
from django.shortcuts import render

from .forms import DataFileUploadForm

from .report_builder import FacebookReportBuilder


class FacebookPostReportView(View):
    template_name = 'facebook_reports/facebook_report_form.html'
    report_template_name = 'facebook_reports/report_templates/post_report.html'

    def get(self, request, *args, **kwargs):
        form = DataFileUploadForm()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = DataFileUploadForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            builder = FacebookReportBuilder()
            report_data = builder.build_post_level_report(form.cleaned_data['data_file'])

            print report_data['end_date']

            return render(request, self.report_template_name,
                          {'client': form.cleaned_data['client'],
                           'start_date': report_data['start_date'],
                           'end_date': report_data['end_date'],
                           'top_posts': report_data['top_posts'],
                           'bottom_posts': report_data['bottom_posts']})
        else:
            return render(request, self.template_name,
                          {'form': form})

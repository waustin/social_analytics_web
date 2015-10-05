from django.views.generic import View
from django.shortcuts import render

from .forms import DataFileUploadForm

from .report_builder import FacebookCsvExportReportBuilder


class FacebookPostReportView(View):
    template_name = 'facebook_reports/facebook_post_report_form.html'
    report_template_name = 'facebook_reports/report_templates/post_report.html'

    def get(self, request, *args, **kwargs):
        form = DataFileUploadForm()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = DataFileUploadForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            builder = FacebookCsvExportReportBuilder()
            report_data = builder.build_post_level_report(form.cleaned_data['data_file'])

            return render(request, self.report_template_name,
                          {'client': form.cleaned_data['client'],
                           'start_date': report_data['start_date'],
                           'end_date': report_data['end_date'],
                           'top_posts': report_data['top_posts'],
                           'bottom_posts': report_data['bottom_posts']})
        else:
            return render(request, self.template_name,
                          {'form': form})


class FacebookPageReportView(View):
    template_name = 'facebook_reports/facebook_page_report_form.html'
    report_template_name = 'facebook_reports/report_templates/page_report.html'

    def get(self, request, *args, **kwargs):
        form = DataFileUploadForm()
        return render(request, self.template_name,
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = DataFileUploadForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            builder = FacebookReportBuilder()
            report_data = builder.build_page_level_report(form.cleaned_data['data_file'])
            return render(request, self.report_template_name,
                          {'client': form.cleaned_data['client'],
                           'start_date': report_data['start_date'],
                           'end_date': report_data['end_date'],
                           'chart_labels': report_data['chart_labels'],
                           'reach': report_data['reach'],
                           'impressions': report_data['impressions'],
                           'engaged_users': report_data['engaged_users'],
                           'likes': report_data['likes']})
        else:
            return render(request, self.template_name,
                          {'form': form})


class FacebookGraphPageReport(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'facebook_reports/facebook_graph_page_report_form.html')

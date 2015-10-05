from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import facebook
import datetime


from facebook_reports.report_builder import FacebookGraphReportBuilder


def parse_date_values(date_values):
    dates = []
    values = []
    for i in date_values:
        dates.append(datetime.datetime.strptime(i['end_time'][:10], '%Y-%m-%d'))
        #dates.append(i['end_time'][:10])
        values.append(int(i['value']))

    return (dates, values)


def parse_fb_data(data):
    REACH_KEY = 'page_impressions_unique'
    ENGAGED_KEY = 'page_engaged_users'
    IMPRESSIONS = 'page_impressions'
    STORIES = 'page_stories'
    STORYTELLERS = 'page_storytellers'
    FANS = 'page_fans'

    for i in data:
        if i['name'] == REACH_KEY:
            tmp = parse_date_values(i['values'])
    return tmp


def home(request):
    data = xrange(10)

    access_token = ''
    user = request.user
    page_id = 'me'
    page_id = 'Caboodles'
    page_id = '/Caboodles/insights/'

    chart_labels = []
    chart_data = []

    if user and not user.is_anonymous():
        try:
            social = user.social_auth.get(provider='facebook')
        except ObjectDoesNotExist:
            return render(request, 'home.html', {
                  'data': data,
                  'token': access_token})
        access_token = social.extra_data['access_token']

        fb_builder = FacebookGraphReportBuilder(access_token)
        data = fb_builder.page_level_report('Caboodles')


        # graph = facebook.GraphAPI(access_token=access_token)
        # data = graph.get_object(page_id, period='days_28', since='2015/06/01', until='2015/09/1')


        # data = parse_fb_data(data['data'])

        # chart_labels = [datetime.datetime.strftime(x, "%m/%d/%Y") for x in data[0]]
        # chart_labels.insert(0, 'date')

        # chart_data = data[1]
        # chart_data.insert(0, 'Reach')



    return render(request, 'home.html', {
                  #'chart_labels': chart_labels,
                  'data': chart_data})


def logout(request):
    auth_logout(request)
    return redirect('home')

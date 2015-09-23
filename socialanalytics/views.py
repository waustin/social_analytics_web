from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import facebook
import datetime

def parse_date_values(date_values):
    return [{'date': datetime.datetime.strptime(i['end_time'][:10], '%Y-%m-%d'), 'value':i['value']} for i in date_values]


def parse_fb_data(data):
    REACH_KEY = 'page_impressions_unique'
    ENGAGED_KEY = 'page_engaged_users'
    IMPRESSIONS = 'page_impressions'
    STORIES = 'page_stories'
    STORYTELLERS = 'page_storytellers'
    FANS = 'page_fans'

    out_data = {}
    for i in data:
        if i['name'] == REACH_KEY:
            out_data[REACH_KEY] = parse_date_values(i['values'])
    print out_data
    return out_data


def home(request):
    data = xrange(10)

    access_token = ''
    user = request.user
    page_id = 'me'
    page_id = 'Caboodles'
    page_id = '/Caboodles/insights/'
    if user and not user.is_anonymous():
        try:
            social = user.social_auth.get(provider='facebook')
        except ObjectDoesNotExist:
            return render(request, 'home.html', {
                  'data': data,
                  'token': access_token})
        access_token = social.extra_data['access_token']
        graph = facebook.GraphAPI(access_token=access_token)
        data = graph.get_object(page_id, period='days_28', since='2015/06/01', until='2015/09/1')
        data = parse_fb_data(data['data'])
    return render(request, 'home.html', {
                  'data': data})


def logout(request):
    auth_logout(request)
    return redirect('home')

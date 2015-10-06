import csvkit
import datetime
import facebook
from future.utils import viewitems

from utils.data import safe_cast


class FacebookCsvExportReportBuilder(object):
    """ Build Facebook Reports from  a csv export file """
    def build_post_level_report(self, f):
        PERMALINK = 1
        MESSAGE = 2
        POST_DATE = 6
        TOTAL_REACH = 7
        IMPRESSIONS = 10
        post_data = list()

        csv = csvkit.reader(f)
        csv.next()
        csv.next()
        for idx, r in enumerate(csv):
            post_data.append({
                'permalink': r[PERMALINK],
                'pubdate': datetime.datetime.strptime(r[POST_DATE], "%m/%d/%Y %H:%M:%S %p"),
                'message': r[MESSAGE],
                'totalreach': safe_cast(r[TOTAL_REACH], int, 0),
                'impressions': safe_cast(r[IMPRESSIONS], int, 0)})

        start_date = min(post_data, key=lambda i: i['pubdate'])['pubdate']
        end_date = max(post_data, key=lambda i: i['pubdate'])['pubdate']

        sorted_data = sorted(post_data, key=lambda i: i['totalreach'], reverse=True)
        top_posts = sorted_data[:10]
        sorted_data.reverse()
        bottom_posts = sorted_data[:10]

        return {'start_date': start_date,
                'end_date': end_date,
                'top_posts': top_posts,
                'bottom_posts': bottom_posts}

    def build_page_level_report(self, f):
        DATE = 0
        TOTAL_LIKES = 1
        ENGAGED_USERS = 6
        TOTAL_REACH = 26
        IMPRESSIONS = 35

        data = list()

        csv = csvkit.reader(f)
        csv.next()
        csv.next()
        for idx, r in enumerate(csv):
            data.append({
                'date': datetime.datetime.strptime(r[DATE], "%Y-%m-%d"),
                'likes': safe_cast(r[TOTAL_LIKES], int, 0),
                'engaged_users': safe_cast(r[ENGAGED_USERS], int, 0),
                'reach': safe_cast(r[TOTAL_REACH], int, 0),
                'impressions': safe_cast(r[IMPRESSIONS], int, 0)
            })

        start_date = min(data, key=lambda i: i['date'])['date']
        end_date = max(data, key=lambda i: i['date'])['date']

        chart_labels = [datetime.datetime.strftime(x['date'], "%m/%d/%Y") for x in data]
        reach = [x['reach'] for x in data]
        impressions = [x['impressions'] for x in data]
        engaged = [x['engaged_users'] for x in data]
        likes = [x['likes'] for x in data]

        reach.insert(0, 'Reach')
        impressions.insert(0, 'Impressions')
        engaged.insert(0, 'Engaged Users')
        likes.insert(0, 'Page Likes')

        return {
            'start_date': start_date,
            'end_date': end_date,
            'chart_labels': chart_labels,
            'reach': reach,
            'impressions': impressions,
            'engaged_users': engaged,
            'likes': likes
        }


class FacebookGraphReportBuilder(object):
    def __init__(self, access_token):
        self.graph = facebook.GraphAPI(access_token=access_token)

    def parse_page_dataset(self, ds):
        return ds

    def build_report(self, page_id, start_date, end_date):
        data_keys = {
            'REACH': 'page_impressions_unique',
            'ENGAGED': 'page_engaged_users',
            'IMPRESSIONS': 'page_impressions',
            'STORIES': 'page_stories',
            'STORYTELLERS': 'page_storytellers',
            'FANS': 'page_fans'
            }

        object_id = "/{0}/insights/".format(page_id)
        page_data = self.graph.get_object(object_id,
                                          period='days_28',
                                          since=start_date,
                                          until=end_date)
        parsed_data = {}

        for dataset in page_data['data']:
            for (k, v) in viewitems(data_keys):
                if dataset['name'] == v:
                    parsed_data[k] = self.parse_page_dataset(dataset)

        return parsed_data

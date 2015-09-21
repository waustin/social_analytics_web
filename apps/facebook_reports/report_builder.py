import csvkit
import datetime


class FacebookReportBuilder(object):

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
                'totalreach': int(r[TOTAL_REACH]),
                'impressions': int(r[IMPRESSIONS])})

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
                'likes': int(r[TOTAL_LIKES]),
                'engaged_users': int(r[ENGAGED_USERS]),
                'reach': int(r[TOTAL_REACH]),
                'impressions': int(r[IMPRESSIONS])
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



# Code from https://gist.github.com/kgn/e96e7ae71a38447ac614
# Credit to David Keegan on github - https://gist.github.com/kgn

import pprint
import time
import typing
import pandas as pd
import json

import requests


def is_error_response(http_response, seconds_to_sleep: float = 1) -> bool:
    """
    Returns False if status_code is 503 (system unavailable) or 200 (success),
    otherwise it will return True (failed). This function should be used
    after calling the commands requests.post() and requests.get().

    :param http_response:
        The response object returned from requests.post or requests.get.
    :param seconds_to_sleep:
        The sleep time used if the status_code is 503. This is used to not
        overwhelm the service since it is unavailable.
    """
    if http_response.status_code == 503:
        time.sleep(seconds_to_sleep)
        return False

    return http_response.status_code != 200


def get_json(url) -> typing.Union[dict, None]:
    """
    Returns json response if any. Returns None if no json found.

    :param url:
        The url go get the json from.
    """
    response = requests.get(url)
    if is_error_response(response):
        return None
    json_response = response.json()
    return json_response


def get_reviews(app_id, page=1) -> typing.List[dict]:
    """
    Returns a list of dictionaries with each dictionary being one review.

    :param app_id:
        The app_id you are searching.
    :param page:
        The page id to start the loop. Once it reaches the final page + 1, the
        app will return a non valid json, thus it will exit with the current
        reviews.
    """
    reviews: typing.List[dict] = [{}]

    while True:
        url = (f'https://itunes.apple.com/rss/customerreviews/id={app_id}/'
               f'page={page}/sortby=mostrecent/json')
        json = get_json(url)

        if not json:
            return reviews

        data_feed = json.get('feed')

        if not data_feed.get('entry'):
            get_reviews(app_id, page + 1)

        reviews += [
            {
                'review_id': entry.get('id').get('label'),
                'title': entry.get('title').get('label'),
                'author': entry.get('author').get('name').get('label'),
                'author_url': entry.get('author').get('uri').get('label'),
                'version': entry.get('im:version').get('label'),
                'rating': entry.get('im:rating').get('label'),
                'review': entry.get('content').get('label'),
                'vote_count': entry.get('im:voteCount').get('label')
            }
            for entry in data_feed.get('entry')
            if not entry.get('im:name')
        ]

        page += 1


#reviews = get_reviews('341329033')
#print(len(reviews))
#pprint.pprint(reviews)
# https://itunes.apple.com/rss/customerreviews/id=282614216/page=1/sortby=mostrecent/json

# Get list of app_ids in the oringal dataset
original = pd.read_csv('./AppleStore.csv')
data = []
missing = []

y = 0
total = len(original[['id']].values) - 1
for x in range(total):
    response = original[['id']].values[x]
    print('\n' + str(y) + ' / ' + str(total))
    print(str(response[0]))
    try:
        data.append(get_reviews(str(response[0])))
    except:
        print("Missing JSON " + str(response[0]))
        missing.append(str(response[0]))
    y = y + 1
    if y % 100 == 0:
        with open("reviews.json", 'w') as write_file:
            json.dump(data, write_file)

with open("reviews.json", 'w') as write_file:
    json.dump(data, write_file)

# Clean JSON Data and Save in CSV
# Format List > List > Dict
# Future Table Format
# Col = app_id, review_id, 'title', 'author', 'author_url', 'version', 'rating', 'review', 'vote_count'
# Row = each review

data = pd.read_json('reviews.json')

# Data pulled
original = pd.read_csv('./AppleStore.csv')
missing = pd.read_csv('missing.txt', header=None)

df3 = pd.merge(original, missing, how='left', left_on='id', right_on=0) # last row does not seem to match
good = df3[df3[0].isnull()]
good = good[:-1]
good = good.reset_index()

merged = pd.merge(good, data, how='left', left_index=True, right_index=True)

merged = merged.drop(columns=['index', 'Unnamed: 0', 'size_bytes', 'currency', 'price', 'rating_count_tot',
                              'rating_count_ver', 'user_rating', 'user_rating_ver', 'ver', 'cont_rating',
                              'prime_genre', 'sup_devices.num', 'ipadSc_urls.num', 'lang.num', 'vpp_lic',
                              '0_x', '0_y'])

def dict_to_df(df):
    '''

    :param df: Series that is passed by the Dataframe.apply() function
    :return:
    '''
    id_master_df = df[2:].apply(pd.Series)
    id_master_df['id'] = df['id']

    return id_master_df


separated = merged.apply(dict_to_df, axis=1)

final_df = pd.DataFrame([],columns=['review_id', 'title', 'author', 'author_url', 'version', 'rating',
       'review', 'vote_count', 'id'])
for row in separated:
    final_df = final_df.append(row)

final_df.to_csv('reviews_final.csv')


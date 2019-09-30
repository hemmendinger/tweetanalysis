import tweepy
import os


def setup_api():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_CONSUMER_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))
    api = tweepy.API(auth,
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True,
                     retry_count=3,
                     retry_delay=3,
                     )

    return api


def process_tweet_object(tweet):
    output = dict()

    output['sceen_name'] = tweet.screen_name
    output['id'] = tweet.id_str
    output['created_at'] = tweet.created_at  # UTC time
    output['text'] = tweet.text.encode("utf-8")
    output['truncated'] = tweet.truncated
    output['source'] = tweet.source,  # client used to send

    # tweet.coordinates,
    # tweet.place
    output['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
    output['in_reply_to_status_id_str'] = tweet.in_reply_to_status_id_str
    output['in_reply_user_id_str'] = tweet.in_reply_to_user_id_str

    # author
    output['auth_id'] = tweet.user.id_str
    output['auth_screen_name'] = tweet.user.screen_name
    output['auth_verified'] = tweet.user.verified
    output['auth_followers_count'] = tweet.user.followers_count
    output['auth_following_count'] = tweet.user.friends_count  # Note: We change it to followers
    output['auth_favs_count'] = tweet.user.favourites_count
    output['auth_statuses_count'] = tweet.user.statuses_count


    if hasattr(tweet, 'quoted_status_id_str'):
        output['quoted_status_id_str'] = tweet.quoted_status_id_str

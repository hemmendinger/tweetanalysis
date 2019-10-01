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


def get_tweet_obj(screen_name: str, api):
    """Derivative of https://gist.github.com/brenorb/1ec2afb8d66af850acc294309b9e49ea"""
    



def process_tweet_object(tweet):
    """Process select Twitter API tweet object attribute values into a dict
    :param tweet: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    :return: dict
    """
    output = dict()

    output['sceen_name'] = tweet.screen_name
    # Convention: Will omit str on attribute name and default to always using str for attributes
    output['id'] = tweet.id_str
    output['created_at'] = tweet.created_at  # UTC time
    output['text'] = tweet.text  # Try without utf encoding
    output['truncated'] = tweet.truncated
    output['source'] = tweet.source,  # client used to send

    # TODO tweet.coordinates,
    # TODO tweet.place

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

    # Note: It's not "is_quoted_status" past tense
    if tweet.is_quote_status or hasattr('retweeted_status', tweet):
        # This likely requires more work as a RT can contain a quoted RT of a quoted RT and so on

        if tweet.is_quote_status:
            output['quoted_status_id'] = tweet.quoted_status_id_str

        # TODO retweeted_status
        rt = tweet.retweeted_status
        output['rt_sceen_name'] = rt.user.screen_name
        # Convention: Will omit str on attribute name and default to always using str for attributes
        output['rt_id'] = rt.id_str
        output['rt_created_at'] = rt.created_at  # UTC time
        output['rt_text'] = rt.text
        output['rt_truncated'] = rt.truncated
        output['rt_source'] = rt.source,  # client used to send
        # TODO quoted_status which contains object of original quoted tweet
        # Have case where is_quote_status is True but has retweeted_status instead of quoted_status
        # Might make more sense to


    # TODO Entities which have been parsed out of the text of the Tweet. Additionally see Entities in Twitter Objects . Example:
    # TODO extended_entities
    # TODO Test case where tweet is media, such as video or image and no text


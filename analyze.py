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


def get_tweet_objects(screen_name: str, api):
    """Credit: This is a derivative of https://gist.github.com/brenorb/1ec2afb8d66af850acc294309b9e49ea
    Only return a list unmodified API objects
    Twitter only allows access to a users most recent 3240 tweets with this method

    Does not always get tweets for unknown reason:
        Worse with the president's twitter account
    """
    # container for all tweepy tweet objects
    tweets = list()

    # initial request for most recent tweets (200 is the maximum allowed count)
    next_tweets = api.user_timeline(screen_name=screen_name, count=200)
    tweets.extend(next_tweets)
    print("{} initial tweets downloaded".format(len(tweets)))

    # save the id of the oldest tweet less one
    oldest = tweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(next_tweets) > 0:
        print("getting tweets before {}".format(oldest))

        # all subsequent requests use the max_id param to prevent duplicates
        next_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        tweets.extend(next_tweets)

        # update the id of the oldest tweet less one
        oldest = tweets[-1].id - 1

        print("...{} tweets downloaded so far".format(len(tweets)))

    return tweets


def process_tweet_object(tweet):
    """Process select Twitter API tweet object attribute values into a dict
    Many attributes are renamed to match how they are commonly described
    For now, it seems easier to maintain if it is quoted RT, and treat all fields as rt_*
    This is a minimal viable processor which may not handle all cases elegantly.
    :param tweet: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
    :return: dict
    """
    output = dict()

    # TODO mistake? output['screen_name'] = tweet.screen_name
    # Convention: Will omit str on attribute name and default to always using str for attributes
    output['screen_name'] = tweet.user.screen_name
    output['id'] = tweet.id_str
    output['created_at'] = tweet.created_at  # UTC time
    output['text'] = tweet.text  # Try without utf encoding
    output['truncated'] = tweet.truncated
    output['source'] = tweet.source,  # client used to send

    # TODO tweet.coordinates, tweet.place
    output['coordinates'] = False if tweet.coordinates is None else True

    output['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
    output['in_reply_to_tweet_id'] = tweet.in_reply_to_status_id_str
    output['in_reply_user_id'] = tweet.in_reply_to_user_id_str
    # TODO Do we want reply text?

    # author
    output['auth_id'] = tweet.user.id_str
    output['auth_screen_name'] = tweet.user.screen_name
    output['auth_verified'] = tweet.user.verified
    output['auth_followers_count'] = tweet.user.followers_count
    output['auth_following_count'] = tweet.user.friends_count  # Note: We change it to followers
    output['auth_favs_count'] = tweet.user.favourites_count
    output['auth_tweet_count'] = tweet.user.statuses_count


    rt = None
    # TODO Order might matter for rt overwrites, verify
    if hasattr(tweet, 'retweeted_status'):
        # This could need more work as a RT can contain a quoted RT of a quoted RT and so on
        output['rt'] = True
        rt = tweet.retweeted_status
    else:
        output['rt'] = False

    # Note: It's not "is_quoted_status" past tense
    if tweet.is_quote_status:
        if hasattr(tweet, 'quoted_status'):
            output['quoted_rt'] = True
            rt = tweet.quoted_status
    else:
        output['quoted_rt'] = False

    if rt is not None:
        output['rt_tweet_id'] = rt.id_str
        output['rt_auth_screen_name'] = rt.author.screen_name
        output['rt_auth_id'] = rt.author.id_str
        output['rt_created_at'] = rt.created_at  # UTC time
        output['rt_text'] = rt.text
        output['rt_truncated'] = rt.truncated
        output['rt_source'] = rt.source,  # client used to send

    # TODO "Entities which have been parsed out of the text of the Tweet. Additionally see Entities in Twitter Objects."
    # TODO extended_entities

    return output



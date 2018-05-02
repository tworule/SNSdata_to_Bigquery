import json
import requests
import sys
import datetime
import time
import pandas
import tweepy
from TwitterAPI import TwitterAPI
from tweepy import Stream
from tweepy import OAuthHandler
sys.stdout.flush()


def instagram_api(keyword):
    url1 = 'https://www.instagram.com/web/search/topsearch/?query='
    url2 = keyword
    url = url1 + url2

    response = requests.get(url)
    response_data = response.json()

    # GET FOLLOWER COUNT & HASHTAG COUNT
    follower_count = response_data['users'][0]['user']['follower_count']
    hashtag_count = 0
    for hashtag in response_data['hashtags']:
        hashtag_count += hashtag['hashtag']['media_count']

    return(follower_count, hashtag_count)


def youtube_api(user_id):
    key = 'AIzaSyA6zFRJ8ZyFOqpJWDAlAHXc27Bu6qjwEGo'
    url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + user_id + "&key=" + key
    # User Name으로 접근하기
    #url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name+"&key="+key

    response = requests.get(url)
    response_data = response.json()

    out_data = response_data['items'][0]['statistics']
    return(int(out_data['viewCount']), int(out_data['commentCount']), int(out_data['subscriberCount']), int(out_data['videoCount']))


def twitter_api(keyword):
    # twitter api는 공백, 특수문자 제거 필요.
    keyword = keyword.replace(" ","")
    keyword = keyword.replace("\'","")
    keyword = keyword.replace("\"","")
    
    # Consumner_key & Secret / Access_Token & Secret
    consumer_key = "3lPwqrJtI2EN3293fPTiYR5YZ"
    consumer_secret = "ThpGRJWnxZrxCGwnkEYhUfSt6BsK7HYbPlQJeYjgtorIlVgpqy"

    access_token = "970479249709649922-iuhXCdUGCLdAFGaYEAkV37QsHoUCBRS"
    access_token_secret = "ie4AtldvfzbfZFvQ9iJcHPGqJbud6GG1SMbHn7f1L3vzZ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Get user's information -> follower count, favorite count, friends count, listed count
    user = api.get_user(keyword)

    return(user.followers_count, user.favourites_count, user.friends_count, user.listed_count)



""" 자동으로 시간별 데이터 쌓기 (기간 단위 = 1분으로 Test)"""
print('Start Test & nohup out test', flush=True)

# SETTING
test_term = 60     # term = seconds (test: 1분씩 갱신 -> 1주일씩 갱신하려면 test_term = 60*60*24*7)

res_list = ['pizza hut','burger king','subway','wendys','KFC','papajohns','popeyes','domino pizza']  # should be eatstreet's res (4000 개)
youtube_id_list = ['UCmHNk3DjDiDzuVrj0aiprZQ', 'UC23ZqC2LTzl7dfOi6EmwJhg', 'UCRoNIIMxKS_LjPH8nAM25ag', 'UCxXHHbiGUO3RziA5kW0m1qw',
                    'UCR8RWMHZcSgqjD0HiUiJ_cQ', 'UC4Qqag_OPteBcE_DrTe2qlg', 'UCBEZh6fiU1m_7uf3JnLObZQ', 'UCO1328RJ5y-TrR2oRq9fBYw']
                                                            #youtube id list 검색으로 자동으로 찾는 방법 리서치 필요함!

# WHILE LOOP
test_count = 0  # Test시에는 무한루프가 최대 3번 돌도록 설정
test_limit = 2

while(True):
    date_list = []
    name_list = []
    instagram_follow_count_list = []
    instagram_hashtag_count_list = []
    youtube_view_count_list = []
    youtube_comment_count_list = []
    youtube_subscriber_count_list = []
    youtube_video_count_list = []
    twitter_follower_count_list = []
    twitter_favorite_count_list = []
    twitter_friends_count_list = []
    twitter_listed_count_list = []

    if test_count == test_limit:
        print("FINISH", flush = True)
        break
    test_count += 1
    
    time.sleep(test_term)
    now = datetime.datetime.now()
    time_key = now

    for i in range(len(res_list)):
        time.sleep(60)  # Twitter api -> call 당 time.sleep(60) 필요함
        tem_list = []
        insta_follower, insta_hashtag = instagram_api(res_list[i])
        if res_list[i] == 'domino pizza':  # Twitter 에서는 domino pizza로 검색하면 안되고, dominos로 해야함
            twit_follower, twit_favorites, twit_friends, twit_listed = twitter_api('dominos')
        else:
            twit_follower, twit_favorites, twit_friends, twit_listed = twitter_api(res_list[i])
        youtub_view, youtub_comment, youtub_subscriber, youtub_video =youtube_api(youtube_id_list[i])

        date_list.append(time_key)
        name_list.append(str(res_list[i]))
        instagram_follow_count_list.append(insta_follower)
        instagram_hashtag_count_list.append(insta_hashtag)
        youtube_view_count_list.append(youtub_view)
        youtube_comment_count_list.append(youtub_comment)
        youtube_subscriber_count_list.append(youtub_subscriber)
        youtube_video_count_list.append(youtub_video)
        twitter_follower_count_list.append(twit_follower)
        twitter_favorite_count_list.append(twit_favorites)
        twitter_friends_count_list.append(twit_friends)
        twitter_listed_count_list.append(twit_listed)

    df = pandas.DataFrame({'date' : date_list, 'name' : name_list, 'instagram_follow_count' : instagram_follow_count_list,
                    'instagram_hashtag_count' : instagram_hashtag_count_list, 'youtube_view_count' : youtube_view_count_list,
                    'youtube_comment_count' : youtube_comment_count_list, 'youtube_subscriber_count' : youtube_subscriber_count_list,
                    'youtube_video_count' : youtube_video_count_list, 'twitter_follower_count' : twitter_follower_count_list,
                    'twitter_favorite_count' : twitter_favorite_count_list, 'twitter_friend_count' : twitter_friends_count_list,
                    'twitter_listed_count' : twitter_listed_count_list})

    pandas.DataFrame.to_gbq(df, 'SNS_data.test', 'datamingo', if_exists = 'append', chunksize = 10000, verbose = True)
    print(datetime.datetime.now(), 'big query update!', flush=True)
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


def youtube_id_mapping(input_list):
    out_list = []
    for i in input_list:
        q = i
        key = "AIzaSyCXfJz6Z8X30I9GgFg14z2M6sQfhNObo5U"
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + q + "&type=channel" + "&key=" + key
        response = requests.get(url)
        response_data = response.json()
        out_list.append(response_data['items'][0]['id']['channelId'])

    return out_list


def youtube_api(user_id):
    key = 'AIzaSyCXfJz6Z8X30I9GgFg14z2M6sQfhNObo5U'
    url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + user_id + "&key=" + key
    # User Name으로 접근하기
    #url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name+"&key="+key

    response = requests.get(url)
    response_data = response.json()

    out_data = response_data['items'][0]['statistics']
    return(int(out_data['viewCount']), int(out_data['commentCount']), int(out_data['subscriberCount']), int(out_data['videoCount']))


def twitter_api(keyword):
    # Consumner_key & Secret / Access_Token & Secret
    consumer_key = "mq7ecRYTpx3OXcF6E5pCTGZTF"
    consumer_secret = "tRboVBFKrnxAXEjaNwwBRfWgZAqXowETSqKOtdSU4RNZUM9NSG"

    access_token = "991892597391081473-sXwXOYP253t85KWEBrqs3WPpOu7its4"
    access_token_secret = "pPiDRxsb5CZjdyZXZahzlFBl1xwfQ7hTTVxLJdKbA4xwd"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # Get user's information -> follower count, favorite count, friends count, listed count
    user = api.search_users(keyword)
    user = user[0]
    return(user['followers_count'], user['favourites_count'], user['friends_count'], user['listed_count'])






###############################################################
# 자동으로 시간별 데이터 쌓기 (기간 단위 = 5분으로 Test)
###############################################################
print('Start Test & nohup out test', flush=True)

# SETTING
test_term = 60*5     # term = seconds (test: 5분씩 갱신 -> 1주일씩 갱신하려면 test_term = 60*60*24*7)
res_list = ["Nando’s", "KFC", "Subway", "Burger King","Pizza Hut", "Domino’s", "Carl’s JR.", "Green Burrito",
            "McDonald’s", "Dunkin’ Donuts", "Tacobell", "Auntie Anne’s", "Cinnabon","Charleys Philly Steak",
            "Quiznos", "Nathan’s Famous", "Red Robin", "Gourmet Burgers and Brew","Shake shack",
            "Five Guys", "Chipotle", "In-N-Out", "Jack in the box"]      #release(1) company list


# Res name -> HASHTAG 때문에 특수문자 제거 필요
tem_res_list = []
for i in res_list:
    tem = i.replace("\'","")
    tem = tem.replace("’","")
    tem = tem.replace(".","")
    tem = tem.replace(",","")
    tem = tem.replace("-","")
    tem_res_list.append(tem)

res_list = tem_res_list
youtube_id_list = youtube_id_mapping(res_list) # 각 식당에 대한 유튜브 id 맵핑


# WHILE LOOP
test_count = 0  # Test시에는 무한루프가 최대 100번 돌도록 설정
test_limit = 100

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
    time_key = datetime.datetime.now()

    for i in range(len(res_list)):
        time.sleep(60)  # Twitter api -> call 당 time.sleep(60) 필요함
        tem_list = []
        try:
            insta_follower, insta_hashtag = instagram_api(res_list[i])
        except:
            insta_follower, insta_hashtag = 0,0

        try:
            twit_follower, twit_favorites, twit_friends, twit_listed = twitter_api(res_list[i])
        except:
            twit_follower, twit_favorites, twit_friends, twit_listed = 0,0,0,0

        try:
            youtub_view, youtub_comment, youtub_subscriber, youtub_video =youtube_api(youtube_id_list[i])
        except:
            youtub_view, youtub_comment, youtub_subscriber, youtub_video = 0,0,0,0
       
        date_list.append(time_key)


        #BIG QUERY에 쌓을 때 레스토랑 네임 -> 소문자, 공백제거로 통일
        res_name = str(res_list[i]).lower()
        res_name = res_name.replace(" ","")
        name_list.append(res_name)

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

    pandas.DataFrame.to_gbq(df, 'SNS_data.last_test', 'datamingo', if_exists = 'append', chunksize = 10000, verbose = True)
    print(datetime.datetime.now(), 'big query update!', flush=True)
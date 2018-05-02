import tweepy
from TwitterAPI import TwitterAPI
from tweepy import Stream
from tweepy import OAuthHandler
import json
#from tweepy.streaming import StreamListener
#from nltk.sentiment.vader import SentimentIntensityAnalyzer as Vader
#import csv

##############################################################################
# Get Tweets -> 모든 트윗 내용, 트윗 작성 날짜 까지 가지고 올 수 있지만, api limit error
##############################################################################
"""
MAX_TWEETS = 5000000000000
tweets = tweepy.Cursor(api.search, q='burgerking', rpp=100).items(MAX_TWEETS)

for tweet in tweets:
    print('----------------------')
    print(tweet.created_at)
    print(tweet.text)
    print('----------------------')
"""

##############################################################################
# Get Tweets -> 한번에 최대 200개 tweet까지 가져올 수 있음.
#            -> 200개씩 여러번 가져오는 방식으로 더 많은 tweet 가져올 수는 있음.
##############################################################################
"""
new_tweets = api.user_timeline(screen_name = 'burgerking',count=200, tweet_mode="extended")
tweets = [[tweet.full_text] for tweet in new_tweets]
print(tweets)
print(len(tweets))
"""

##############################################################################
# Get Tweets & Sentiment Analysis -> 시간 엄~청 오래 걸림
##############################################################################
"""
ckey = consumer_key
csecret = consumer_secret
atoken = access_token
asecret = access_token_secret

class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        sid=Vader()
        ss=sid.polarity_scores(tweet)
        
        if ss['pos']>0 and ss['compound']>0:
            sentimentalStatus='Positive'
        elif ss['neg']>0 and ss['compound']<0:
            sentimentalStatus='Negative'
        else:
            sentimentalStatus='neutural'
            
        print(tweet+"\n [compound score] : "+sentimentalStatus)
        output=open("twitterout1.txt","a",encoding='utf-8')
        output.write(tweet)
        output.write("Sentimental Status:"+sentimentalStatus)
        output.write("\n")
        output.close()
        time.sleep(1)
        return True
    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["burgerking"])
print_test = twitterStream.filter(track=["burgerking"])
"""
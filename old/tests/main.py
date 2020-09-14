import os
import time

from utils import apis

def main():
    tweepy, api = apis.get_tweepy_api()

    search_words = "game of thrones"
    date_since = "2019-01-01"

    iterator = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since).items(5)

    with open('tweets.txt', 'w') as output:
        print(time.ctime())
        count = 0
        for tweet in iterator:
            count += 1
            output.write(f"[{count}]: {tweet.text}\n\n")
            if count % 100 == 0:
                print(count)
            if count > 1000:
                break
        print(time.ctime())

if __name__ == "__main__":
    main()
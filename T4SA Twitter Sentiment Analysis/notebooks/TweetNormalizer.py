# Requires normalise and data from nltk
# https://github.com/EFord36/normalise
# https://www.nltk.org/data.html
# Dependencies:
#   -   Install normalise to the python environment
#   -   Install nltk to the python environment
#       The import code below should install the right nltk data set dependencies

import sqlite3
import csv
import normalise
import nltk
for dependency in ("brown", "names", "wordnet", "averaged_perceptron_tagger", "universal_tagset"):
    nltk.download(dependency)
import os
import sys
import re

class TweetNormalizer:

    CONFIG_NORM_HASHTAGS = "normalize_hashtags"
    CONFIG_REMOVE_LINKS = "remove_links"
    CONFIG_REMOVE_MENTIONS = "remove_mentions"
    CONFIG_REMOVE_ARTIFACTS = "remove_artifacts"

    _known_fields = [CONFIG_NORM_HASHTAGS, CONFIG_REMOVE_LINKS, CONFIG_REMOVE_MENTIONS, CONFIG_REMOVE_ARTIFACTS]
    _default_config = {
        CONFIG_NORM_HASHTAGS : False,
        CONFIG_REMOVE_LINKS : True,
        CONFIG_REMOVE_MENTIONS : True,
        CONFIG_REMOVE_ARTIFACTS : True
    }

    _weekday_abbreviations = {
        "Fri" : "Friday"
    }

    _twitter_abbreviations = {
        "SEO" : "search engine optimization",
        "SROI" : "social return on investment",
        "SN" : "social network",
        "YT": "YouTube",
        "UGC" : "user generated content",
        "SMO" : "social media optimization",
        "FB" : "Facebook",
        "LI" : "LinkedIn",
        "SM": "social media",
        "SMM" : "social media marketing",
        "BGD" : "background",
        "BTW" : "by the way",
        "ABT" : "about",
        "AFAIK" : "as far as I know",
        "AYFKMWTS": "are you fucking kidding me with this shit",
        "BR" : "best regards",
        "CUL8R": "see you later",
        "FML": "fuck my life",
        "FUBAR" : "fucked up beyond all repair",
        "BBFN" : "bye bye for now",
        "B4" : "before",
        "EMA" : "email address",
        "DYK" : "do you know",
        "FTF" : "face to face",
        "F2F" : "face to face",
        "HAGN" : "have a good night",
        "FOTD" : "find of the day",
        "FTW" : "for the win",
        "FWIW" : "for what it's worth",
        "HTH" : "hope that helps",
        "ICYMI" : "in case you missed it",
        "HOTD" : "headline of the day",
        "IIRC" : "if I remember correctly",
        "KK" : "ok",
        "IC" : "i see",
        "IDK" : "I don't know",
        "IMHO" : "in my humble opinion",
        "ORLY" : "oh really",
        "YOYO" : "you're on your own",
        "LMAO" : "laughing my ass off",
        "IRL" : "in real life",
        "JK" : "just kidding",
        "LOL" : "laugh our loud",
        "LML" : "let me know",
        "JSYK" : "just so you know",
        "NSFW" : "not safe for work",
        "NBD" : "no big deal",
        "OMG" : "oh my god",
        "QOTD" : "quote of the day",
        "SMH" : "shaking my head",
        "TY" : "thank you",
        "SRS" : "serious",
        "STFU" : "shut the fuck up",
        "SMDH" : "shaking my damn head",
        "TYIA" : "thank you in advance",
        "TLDR" : "too long, didn't read",
        "TWB" : "tweet me back",
        "TYVW" : "thank you very much",
        "WTV": "whatever",
        "YMMV" : "your mileage may vary",
        "WE" : "whatever",
        "YKWIM" : "you know what I mean",
        "YOLO" : "you only live once",
        "YGTR" : "you got that right",
        "FAV" : "favorite",
        "ASAP" : "as soon as possible"
    }

    _finance_abbreviations = {
        "CAGR" : "compound annual growth rate",
        "CAPEX" : "capital expenditures",
        "COB" : "close of business",
        "EPS" : "earnings per share",
        "LLC" : "limited liability company",
        "MTD" : "month to date",
        "NAV" : "net asset value",
        "NCND" : "non-circumvent and non-disclosure",
        "NDA" : "non disclosure agreement",
        "P&L" :  "profit and loss",
        "P/E" : "price to earnings ratio",
        "QTD" : "quarter to  date",
        "ROA" : "return on assets",
        "ROCE" : "return On capital employed",
        "ROE" : "return on equity",
        "ROI" : "return on investment",
        "ROIC" : "return on invested capital",
        "RONA" : "return on net assets",
        "ROS" : "return on sales",
        "SIV" : "structured investment vehicle",
        "TSR" : "total shareholder return",
        "WC" : "working capital",
        "YTD"  : "year to date"
    }

    _twitter_artifacts = ["MT", "RT", "DM", "PRT", "HT", "CC"]

    def __init__(self, config=None):
        self._config = config
        self._abbreviations = {}
        self.create_abbreviations()

    def create_abbreviations(self):
        self._abbreviations.update(TweetNormalizer._twitter_abbreviations)
        self._abbreviations.update(TweetNormalizer._finance_abbreviations)
        self._abbreviations.update(TweetNormalizer._weekday_abbreviations)

        lower_case_abbreviations = {}

        for key in self._abbreviations:
            lower_case_abbreviations[key.lower()] = self._abbreviations[key]

        self._abbreviations.update(lower_case_abbreviations)

    def get_config_field(self, field:str):
        if self._config is not None and field in self._config:
            return self._config[field]
        else:
            return TweetNormalizer._default_config[field]

    def _read_tweets(self, file_name: str, limit:int=None)->list:
        '''
        :param file_name: a CSV file containing two columns: tweet ID, tweet text
        :return: a list of tuples of the form (tweet ID, list of space-separated tokens in tweet)
        '''

        rows = []
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for i,row in enumerate(reader):
                if(i==0):   #skip header
                    continue
                elif limit is not None and i>limit: #stop at limit
                    break

                id = row[0]

                tweet_token_list = []
                for tok in row[1:]:
                    tweet_token_list += tok.split(" ")

                rows.append((id, tweet_token_list))

        return rows

    @staticmethod
    def is_hashtag(token: str):
        return (token[0] == "#")

    def normalize_hashtag(self, token: str):
        return normalise.normalise(token, verbose=False, variety="AmE", user_abbrevs=self._abbreviations) if self.get_config_field(TweetNormalizer.CONFIG_NORM_HASHTAGS) else token  # don't change it

    @staticmethod
    def is_link(token: str):
        return (token.find("http://") == 0) or (token.find("https://") == 0)

    def normalize_link(self, token: str):
        return "" if self.get_config_field(TweetNormalizer.CONFIG_REMOVE_LINKS) else token

    @staticmethod
    def is_mention(token: str):
        return (token[0] == "@")

    def normalize_mention(self, token: str):
        return "" if self.get_config_field(TweetNormalizer.CONFIG_REMOVE_MENTIONS) else token

    @staticmethod
    def is_artifact(token: str, is_first_token: bool):
        return is_first_token and (token in TweetNormalizer._twitter_artifacts)

    def normalize_artifact(self, token: str):
        return "" if self.get_config_field(TweetNormalizer.CONFIG_REMOVE_ARTIFACTS) else token

    def remove_puctuation(self, token:str):
        new_token = re.sub(r'[!()-[]{};:'"\, <>./?$%^&*_~]', '', token)
        return new_token.strip()

    def normalize_to_csv(self, raw_tweet_file: str, norm_tweet_file:str=None, tweet_limit:int=None):
        norm_file = os.path.splitext(raw_tweet_file)[0] + "_norm.csv"
        if norm_tweet_file is not None:
            norm_file = norm_tweet_file

        tweets = self._read_tweets(raw_tweet_file, tweet_limit)

        tweet_idx = 0
        with open(norm_file, 'w', newline='') as normed_tweets_file:
            norm_file_writer = csv.writer(normed_tweets_file)

            print(f"Normalizing {tweet_limit if tweet_limit is None else len(tweets)} tweets")

            for tweet in tweets:
                norm_tweet = []     # all the normed tokens from each token in the tweet
                print(f"Normalizing Tweeet ID {tweet[0]}, Tweet # {tweet_idx}")

                is_first_token = True
                for token in tweet[1]:
                    norm_tokens = []    # the normed token(s) from this token in the tweet
                    try:
                        #remove punctuation to start
                        token = self.remove_puctuation(token)
                        if token == "":
                            is_first_token = False
                            continue

                        if self.is_artifact(token, is_first_token):
                            norm_tokens.append(self.normalize_artifact(token))
                        elif self.is_hashtag(token):
                            norm_tokens.append(self.normalize_hashtag(token))
                        elif self.is_link(token):
                            norm_tokens.append(self.normalize_link(token))
                        elif self.is_mention(token):
                            norm_tokens.append(self.normalize_mention(token))
                        else:
                            norm_tokens += normalise.normalise(token, verbose=False, variety="AmE", user_abbrevs=self._abbreviations)

                        # if normalise just expanded the letters of an abbreviation then use the original token
                        if "".join(norm_tokens).replace(" ", "") == token:
                            norm_tokens = [token]
                    except:
                        e = sys.exc_info()[0]
                        norm_tokens = [token]  # use the original token if we failed to normalize it
                    norm_tweet += norm_tokens
                    is_first_token = False

                norm_file_writer.writerow([tweet[0], " ".join(norm_tweet).strip()])
                tweet_idx += 1


if __name__ == "__main__":
    file_path = "raw_tweets_text.csv"
    norm_path_base = "norm_tweet_text"
    limit = 4000

    output_file = norm_path_base+"_default.csv"
    print("Generating " + output_file)
    t = TweetNormalizer()
    t.normalize_to_csv(file_path, norm_path_base+"_default.csv", tweet_limit=limit)

'''
    output_file = norm_path_base + "_norm_hashtags.csv"
    print("Generating " + output_file)
    t = TweetNormalizer(config={TweetNormalizer.CONFIG_NORM_HASHTAGS: True})
    t.normalize_to_csv(file_path, norm_path_base + "_norm_hashtags.csv", tweet_limit=limit)

    output_file = norm_path_base + "_links.csv"
    print("Generating " + output_file)
    t = TweetNormalizer(config={TweetNormalizer.CONFIG_REMOVE_LINKS: False})
    t.normalize_to_csv(file_path, norm_path_base + "_links.csv", tweet_limit=limit)

    output_file = norm_path_base + "_links_mentions.csv"
    print("Generating " + output_file)
    t = TweetNormalizer(config={TweetNormalizer.CONFIG_REMOVE_LINKS: False, TweetNormalizer.CONFIG_REMOVE_MENTIONS: False})
    t.normalize_to_csv(file_path, norm_path_base + "_links_mentions.csv", tweet_limit=limit)
'''






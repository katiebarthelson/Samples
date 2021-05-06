import click
import json
import logging
import normalise
import multiprocessing
import concurrent
import sys
import os
from os import listdir
from os.path import isfile, join, basename
import string

logger = logging.getLogger(__name__)

weekday_abbreviations = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday"
}
twitter_abbreviations = {
    "SEO": "search engine optimization",
    "SROI": "social return on investment",
    "SN": "social network",
    "YT": "YouTube",
    "UGC": "user generated content",
    "SMO": "social media optimization",
    "FB": "Facebook",
    "LI": "LinkedIn",
    "SM": "social media",
    "SMM": "social media marketing",
    "BGD": "background",
    "BTW": "by the way",
    "ABT": "about",
    "AFAIK": "as far as I know",
    "AYFKMWTS": "are you fucking kidding me with this shit",
    "BR": "best regards",
    "CUL8R": "see you later",
    "FML": "fuck my life",
    "FUBAR": "fucked up beyond all repair",
    "BBFN": "bye bye for now",
    "B4": "before",
    "EMA": "email address",
    "DYK": "do you know",
    "FTF": "face to face",
    "F2F": "face to face",
    "HAGN": "have a good night",
    "FOTD": "find of the day",
    "FTW": "for the win",
    "FWIW": "for what it's worth",
    "HTH": "hope that helps",
    "ICYMI": "in case you missed it",
    "HOTD": "headline of the day",
    "IIRC": "if I remember correctly",
    "KK": "ok",
    "IC": "i see",
    "IDK": "I don't know",
    "IMHO": "in my humble opinion",
    "ORLY": "oh really",
    "YOYO": "you're on your own",
    "LMAO": "laughing my ass off",
    "IRL": "in real life",
    "JK": "just kidding",
    "LOL": "laugh our loud",
    "LML": "let me know",
    "JSYK": "just so you know",
    "NSFW": "not safe for work",
    "NBD": "no big deal",
    "OMG": "oh my god",
    "QOTD": "quote of the day",
    "SMH": "shaking my head",
    "TY": "thank you",
    "SRS": "serious",
    "STFU": "shut the fuck up",
    "SMDH": "shaking my damn head",
    "TYIA": "thank you in advance",
    "TLDR": "too long, didn't read",
    "TWB": "tweet me back",
    "TYVW": "thank you very much",
    "WTV": "whatever",
    "YMMV": "your mileage may vary",
    "YKWIM": "you know what I mean",
    "YOLO": "you only live once",
    "YGTR": "you got that right",
    "FAV": "favorite",
    "ASAP": "as soon as possible",
    "U": "you"
}
finance_abbreviations = {
    "CAGR": "compound annual growth rate",
    "CAPEX": "capital expenditures",
    "COB": "close of business",
    "EPS": "earnings per share",
    "LLC": "limited liability company",
    "MTD": "month to date",
    "NAV": "net asset value",
    "NCND": "non-circumvent and non-disclosure",
    "NDA": "non disclosure agreement",
    "P&L": "profit and loss",
    "PNL": "profit and loss",
    "P/E": "price to earnings ratio",
    "QTD": "quarter to  date",
    "ROA": "return on assets",
    "ROCE": "return On capital employed",
    "ROE": "return on equity",
    "ROI": "return on investment",
    "ROIC": "return on invested capital",
    "RONA": "return on net assets",
    "ROS": "return on sales",
    "SIV": "structured investment vehicle",
    "TSR": "total shareholder return",
    "YTD": "year to date"
}
custom_abbreviations = {}

twitter_artifacts = ["MT", "RT", "DM", "PRT", "HT", "CC"]


def build_abbreviation_list():
    custom_abbreviations.update(weekday_abbreviations)
    custom_abbreviations.update(twitter_abbreviations)
    custom_abbreviations.update(finance_abbreviations)


def create_output_dir(output_path):
    dirname = os.path.dirname(output_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def get_files_to_normalize(input_path, output_path):
    files_to_normalize = []

    output_path_files = {}
    filenames = [f for f in listdir(output_path) if isfile(join(output_path, f))]
    for file in filenames:
        output_path_files[file] = True

    filenames = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    for file in filenames:
        if file not in output_path_files:
            full_path = join(input_path, file)
            files_to_normalize.append(full_path)

    return files_to_normalize


def norm_thread(text):
    try:
        return normalise.normalise(text, verbose=False, variety="AmE", user_abbrevs=custom_abbreviations)
    except: # don't really care what happened, lets just use the original token
        return text


def normalise_custom(text):
    timeout = 60.0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(norm_thread, text)
        try:
            norm_text = future.result(timeout)
        except concurrent.futures.TimeoutError:
            logger.debug(f"Timed out while normalizing token: {text}")
            cancelled = future.cancel()
            if not cancelled:
                logger.debug(f"Unable to cancel worker thread normalizing token: {text}")
            norm_text = text
        except:
            e = sys.exc_info()[0]
            logger.debug(f"Exception encountered in normalise_custom. Token: {text} Exception: {e}")
            norm_text = text

    return norm_text


def is_hashtag(token):
    return token[0] == "#"


def normalize_hashtag(token):
    return token  # don't change it


def is_link(token):
    return (token.find("http://") == 0) or (token.find("https://") == 0)


def normalize_link(token):
    return token  # don't change it, Google NLP uses links in topic categorization


def is_mention(token):
    return token[0] == "@"


def normalize_mention(token):
    return ""  # remove mentions


def is_artifact(token, is_first_token):
    return is_first_token and (token in twitter_artifacts)


def normalize_artifact(token):
    return ""


def remove_puctuation(token: str):
    replacement_dict = {key: " " for key in string.punctuation}
    replacement_table = str.maketrans(replacement_dict)
    return token.translate(replacement_table)


def tokenize_tweet(text):
    return text.split()


def normalize_text(tweet_text):
    tokens = tokenize_tweet(tweet_text)

    norm_tweet = []  # all the normed tokens from each token in the tweet

    is_first_token = True
    for token in tokens:
        norm_tokens = []  # the normed token(s) from this token in the tweet
        try:
            if is_hashtag(token):
                norm_tokens.append(normalize_hashtag(token))
            elif is_mention(token):
                norm_tokens.append(normalize_mention(token))
            elif is_link(token):
                norm_tokens.append(normalize_link(token))
            else:
                # if not a hashtag, mention or link, remove any punctuation and process the token(s)
                token_no_punc = remove_puctuation(token)
                sub_tokens = tokenize_tweet(token_no_punc)
                for sub_token in sub_tokens:
                    if is_artifact(token, is_first_token):
                        norm_tokens.append(normalize_artifact(sub_token))
                    else:
                        if token != "":
                            norm_tokens += normalise_custom(sub_token)
                            # if normalise just expanded the letters of an abbreviation then use the original token
                            if "".join(norm_tokens).replace(" ", "") == token:
                                norm_tokens = [token]
        except:
            e = sys.exc_info()[0]
            logger.debug(f"Exception encountered. Token: {token} Exception: {e}")
            norm_tokens = [token]  # use the original token if we failed to normalize it

        norm_tweet += norm_tokens
        is_first_token = False

    # rejoin the tokens to re-form the Tweet
    return " ".join(norm_tweet).strip()


def normalize_tweet(args):
    try:
        input_file, output_path = args

        with open(input_file) as fp:
            tweet_data = json.load(fp)

        tweet_text = tweet_data['data']['text']
        tweet_id = tweet_data['data']['id']
        normalized_text = normalize_text(tweet_text)

        output_data = {'data': {'id':tweet_id,'text': normalized_text}}
        output_file = join(output_path, basename(input_file))

        with open(output_file, 'w') as fp:
            json.dump(output_data, fp)

    except Exception as e:
        logger.error(f"Error normalizing tweet {input_file}: {str(e)}")


# for debugging purposes only
def normalize_tweets_serially(tweet_files, output_path):
    logger.info(f"Processing {len(tweet_files)} Tweets Serially")
    for input_file in tweet_files:
        logger.debug(f"{input_file}")
        normalize_tweet((input_file, output_path))
    return True


def normalize_tweets(tweet_files, output_path, timeout=None):
    expected_throughput = 2500  # expecting 2500 per minute due to observing about 3500 per minute on a slow machine
    num_tweets = len(tweet_files)
    default_timeout = num_tweets/expected_throughput

    if timeout is None:
        timeout = default_timeout

    logger.info(f"Processing {len(tweet_files)} Tweets in Parallel ({timeout} minute timeout)")
    input_file_output_path_pairs = []
    for input_file in tweet_files:
        input_file_output_path_pairs.append(
            (input_file, output_path)
        )

    cpu_count = multiprocessing.cpu_count()
    async_res = multiprocessing.Pool(cpu_count * 4).map_async(
        normalize_tweet, input_file_output_path_pairs)

    try:
        async_res.wait(timeout*60.0)
    except:
        logger.info(f"Processing timed out or was killed")

    return async_res.ready()


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def _main(input_path, output_path):
    create_output_dir(output_path)
    build_abbreviation_list()
    files_to_normalize = get_files_to_normalize(input_path, output_path)
    result = normalize_tweets(files_to_normalize, output_path)
    log_statement = "completed" if result else "timed out"
    logger.info(f"Preprocessing {log_statement}")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    _main()

"""Filters the provided file of json-formatted Tweet IDs/language of origin by the provided language and isolates the Tweet IDs for hydration"""
import argparse
import json
import tarfile
from typing import List, Iterable


def filter_and_isolate_tweet_ids(tweet_jsons: Iterable[str], languages: List[str]):
    """Iteratively filters the provided iterable of json-formatted tweet-ids/languages/other information"""
    for tweet_json in tweet_jsons:
        cur_tweet = json.loads(tweet_json)
        if cur_tweet['Twitter_lang'] in languages:
            yield cur_tweet['tweet_id']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infiles', metavar='I', nargs='+',
                        help="The file(s) to read in and from which to isolate Tweet IDs")
    parser.add_argument('-l', '--languages', nargs='+',
                        help="The languages Tweets written in which to include. Example: -l en de")
    parser.add_argument('--tgz', '--targzipped', action='store_true',
                        help="Flag whether the input(s) is/are tarballed/gzipped collections of tweet id information json files")
    args = parser.parse_args()

    infiles = args.infiles
    if args.tgz:
        tarmemberlists = (tarfile.open(tar).members() for tar in args.infiles)
        infiles = (infile for infile in tarmemberlist for tarmemberlist in tarmemberlists)

    for infile in infiles:
        tweet_ids = filter_and_isolate_tweet_ids(infile, args.languages)
        for tweet_id in tweet_ids:
            print(tweet_id)

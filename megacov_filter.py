"""Filters the provided file of json-formatted Tweet IDs/language of origin by the provided language and isolates the Tweet IDs for hydration"""
import argparse
import json
import tarfile
import warnings
from itertools import chain
from typing import List, Iterable

def filter_and_isolate_tweet_ids(tweet_jsons: Iterable[str], languages: List[str], strict_match: bool) -> Iterable[int]:
    """
    Iteratively filters the provided iterable of json-formatted tweet-ids/languages/other information.
    inputs:
    tweet_jsons: an iterable collection of strings, where each string is a json representation that has a tweet_id field and a Twitter_lang or LangID_tool field
    languages: Either a list of two-letter language prefixes to include Tweets of, or None (in which case all Tweet IDs are yielded)
    strict_match: If true, only tweets whose Twitter-identified language matches one of the given languages will remain after filtering.\n\
                  If false, Twitter-unidentified Tweets that have a matching language determined by a separate tool will also remain.\n\
                  (in other words, whether to consider the 'LangID_tool' field in addition to the 'Twitter_lang' field)
    """
    for tweet_json in tweet_jsons:
        cur_tweet = json.loads(tweet_json)
        #If languages is None, perform no filtering. Otherwise, only yield Tweet IDs matching one of the given two-letter language prefixes.
        if (languages is None
                or cur_tweet['Twitter_lang'] in languages
                or cur_tweet['LangID_tool'] in languages and not strict_match):
            yield cur_tweet['tweet_id']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infiles', metavar='I', nargs='+',
                        help="The file(s) to read in and from which to isolate Tweet IDs")
    parser.add_argument('-l', '--languages', nargs='+',
                        help="The languages Tweets written in which to include. Example: -l en de. If no languages are specified, no filtering is performed.")
    parser.add_argument('-s', '--strict', action='store_true',
                        help="Flag whether to filter tweets only by Twitter's identification. If unchecked, includes Tweets tagged using the LangID tool in post")
    parser.add_argument('--tgz', '--targzipped', action='store_true',
                        help="Flag whether the input(s) is/are tarballed/gzipped collections of tweet id information json files")
    args = parser.parse_args()

    if args.languages is None:
        warnings.warn("No languages were specified for filtering. All languages will be included.", stacklevel=2)

    #Determine whether infiles are tarballed/gzipped file collections
    infiles = args.infiles
    if args.tgz:
        tarmemberlists = (tarfile.open(tar).members() for tar in args.infiles)
        infiles = (infile for infile in chain(tarmemberlists))

    #Extract and print Tweet IDs for each of the resulting Tweets after filtering
    for infile in infiles:
        with open(infile) as opened_infile:
            tweet_ids = filter_and_isolate_tweet_ids(tweet_jsons=opened_infile, languages=args.languages, strict_match=args.strict)
            for tweet_id in tweet_ids:
                print(tweet_id)

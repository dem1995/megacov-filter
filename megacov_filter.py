"""Filters the provided file of json-formatted Tweet IDs/language of origin by the provided language and isolates the Tweet IDs for hydration"""
import argparse
import json
import tarfile
import warnings
from contextlib import closing
from typing import List, Iterable, IO

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
    #Parse the arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infiles', metavar='I', nargs='+',
                        help="The file(s) to read in and from which to isolate Tweet IDs")
    parser.add_argument('-l', '--languages', nargs='+',
                        help="The languages Tweets written in which to include. Example: -l en de. If no languages are specified, no filtering is performed.")
    parser.add_argument('-s', '--strict', action='store_true',
                        help="Flag whether to filter tweets only by Twitter's identification. If unchecked, includes Tweets tagged using the LangID tool in post")
    parser.add_argument('--tgz', '--targzipped', action='store_true',
                        help="Flag whether the input(s) is/are tarballed & gzipped collections of tweet id information json files")
    args = parser.parse_args()

    if args.languages is None:
        warnings.warn("No languages were specified for filtering. All languages will be included.", stacklevel=2)

    #Determine whether infiles are tarballed/gzipped file collections, and prepare an iterator over each json file, opened
    def _yield_open_targz_content_files(targzs: Iterable[str]) -> Iterable[IO]:
        """Returns an iterable over open files contained within the provided gzipped targz collections of said files"""
        for targz in targzs:
            with closing(tarfile.open(targz)) as opened_tar:
                tar_members = opened_tar.getmembers()
                for member in tar_members:
                    opened_extracted_file = opened_tar.extractfile(member)
                    yield opened_extracted_file

    def _yield_open_files(closed_files: Iterable[str]) -> Iterable[IO]:
        """Returns an iterable over each of the provided files, opened"""
        for closed_file in closed_files:
            with closing(open(closed_file)) as opened_file:
                yield opened_file

    if args.tgz:
        opened_infiles = _yield_open_targz_content_files(args.infiles)
    else:
        opened_infiles = _yield_open_files(args.infiles)

    #Extract and print Tweet IDs for each of the resulting Tweets (contained within the json files) after filtering
    for opened_infile in opened_infiles:
        tweet_ids = filter_and_isolate_tweet_ids(tweet_jsons=opened_infile, languages=args.languages, strict_match=args.strict)
        for tweet_id in tweet_ids:
            print(tweet_id)

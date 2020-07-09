# Megacov Dataset Filter
Python command-line script for filtering portions of the Megacov Twitter ID dataset (paper [here](https://arxiv.org/abs/2005.06012), files [here](https://github.com/UBC-NLP/megacov)) and isolating the resulting Twitter IDs by themselves for hydration.
## Usage
To use `megacov-filter`, clone the repo (`git clone https://github.com/dem1995/megacov-filter.git`), make sure Python is installed, and run `python megacov_filter <inputfile1 inputfile2...> <outputfile>`. Tarballed+gzipped file collections are supported as inputs by setting the `-tgz` filter. Language filtering is supported by using the argument `-l` along with two-letter prefixes for the desired languages to be included (i.e. `-l en ja`). By default filtering checks to see if any of the languages match either Twitter's interpretation of the Tweet's language (Twitter_lang) or, if that is None, a Twitter ID tool's interpretation (LangID_tool); however, if only the former is desired (as it's ostensibly more strict) the `-s` strict flag can be added.
A more comprehensive description of the various arguments is given in the Help section below.

## Example
Given the input
>{"tweet_id":1222480698642030592,"Twitter_lang":"zh","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-29","country":"N/A","LangID_tool":"N/A"}
>{"tweet_id":1221845540960268288,"Twitter_lang":"ja","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-27","country":"N/A","LangID_tool":"N/A"}
>{"tweet_id":1221845383183093760,"Twitter_lang":"zh","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-27","country":"N/A","LangID_tool":"N/A"}
>{"tweet_id":1221845318595035136,"Twitter_lang":"zh","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-27","country":"N/A","LangID_tool":"N/A"}
>{"tweet_id":1221845057134718983,"Twitter_lang":"zh","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-27","country":"N/A","LangID_tool":"N/A"}
>{"tweet_id":1221844992181690368,"Twitter_lang":"ja","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-27","country":"N/A","LangID_tool":"N/A"}
>{"tweet_id":1221844951341731840,"Twitter_lang":"ja","date_year":2020,"date_month":1,"date_weekOfYear":5,"date":"2020-01-27","country":"N/A","LangID_tool":"N/A"}

Running
`python $DIRECTORY/megacov_filter.py $IN -l ja > $OUT`

Yields
>1221845540960268288
>1221844992181690368
>1221844951341731840

## Help
usage: `megacov_filter.py [-h] [-l LANGUAGES [LANGUAGES ...]] [-s] [--tgz] I [I ...]`

Filters the provided file of json-formatted Tweet IDs/language of origin by the provided language and isolates the Tweet IDs for hydration

positional arguments:
  I                     The file(s) to read in and from which to isolate Tweet IDs

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGES [LANGUAGES ...], --languages LANGUAGES [LANGUAGES ...]
                        The languages Tweets written in which to include. Example: -l en de. If no languages are specified, no filtering is performed.
  -s, --strict          Flag whether to filter tweets only by Twitter's identification. If unchecked, includes Tweets tagged using the LangID tool in post
  --tgz, --targzipped   Flag whether the input(s) is/are tarballed/gzipped collections of tweet id information json files

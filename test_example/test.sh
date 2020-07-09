#!/bin/bash
#Example program to demonstrate Python ID extraction/filtering. Isolates the Tweet IDs with the given language, Japanese (as identified by Twitter).
DIRECTORY=$(cd `dirname $0` && cd .. && pwd)
IN="${DIRECTORY}/test_example/in.txt"
OUT="${DIRECTORY}/test_example/out.txt"
python $DIRECTORY/megacov_filter.py $IN -l ja > $OUT 
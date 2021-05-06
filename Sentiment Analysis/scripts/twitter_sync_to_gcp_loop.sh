#!/bin/bash

while true; do
    mkdir -p data/raw/twitter_staging/
    find data/raw/twitter/ -name '*.json' -exec mv {} data/raw/twitter_staging/ \;

    gsutil -m cp data/raw/twitter_staging/*.json gs://cashification.appspot.com/Tweets/

    rm -rf data/raw/twitter_staging/

    sleep 5
done

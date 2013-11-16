#!/usr/bin/env python2

# Modified Twitter Sentiment Corpus Install Script
# 
# as per the Twitter API v1.1 https://dev.twitter.com/docs/api/1.1/overview
# the original script written by Sanders (http://www.sananalytics.com/lab/twitter-sentiment)
# becomes defunct. The following changes have been made to comply with latest rules of the API
# --> Authentication of requests using oauth
# --> Minor changes to incorporate changes in response format eg use of 'errors' in place of 'error'
#
# PLEASE NOTE :
# Provide your access token and key, and consumer token and key as the global variables declared here. 
# These are provided to you at your application homepage at dev.twitter.com
# 
# You may go through the sanders_readme.pdf file to better understand this script.
# You may also write to me for any help, Ill try and help you to the best of my capability.
# 
# - Karan Luthra
#   karanluthra06@gmail.com
#   14 November, 2013
#
#!!-----Message by original author----------!!
#
# 	Sanders-Twitter Sentiment Corpus Install Script
# 	Version 0.1
#
# 	Pulls tweet data from Twitter because ToS prevents distributing it directly.
#
# 	Right now we use unauthenticated requests, which are rate-limited to 150/hr.
# 	We use 125/hr to stay safe.  
#
# 	We could more than double the download speed by using authentication with
# 	OAuth logins.  But for now, this is too much of a PITA to implement.  Just let
# 	the script run over a weekend and you'll have all the data.
#
# 	  - Niek Sanders
# 	    njs@sananalytics.com
# 	    October 20, 2011
#
#
# 	Excuse the ugly code.  I threw this together as quickly as possible and I
# 	don't normally code in Python.
#

import csv, getpass, json, os, time, urllib, oauth2 as oauth, time

# Provide your access token and key, and consumer token and key as the global variables declared here.
TOKEN_KEY = ""
TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

def check_if_keys_provided():

    # check if access/consumer tokens and keys are provided
    if not (TOKEN_KEY and TOKEN_SECRET and CONSUMER_KEY and CONSUMER_SECRET):
        print ('--> Please edit install.py, and provide all the tokens/keys as global variables declared here.\n')
        raise RuntimeError('error in authentication')

    return

def get_user_params():

    user_params = {}

    # get user input params
    user_params['inList']  = raw_input( '\nInput file [./corpus.csv]: ' )
    user_params['outList'] = raw_input( 'Results file [./full-corpus.csv]: ' )
    user_params['rawDir']  = raw_input( 'Raw data dir [./rawdata/]: ' )
    
    # apply defaults
    if user_params['inList']  == '': 
        user_params['inList'] = './corpus.csv'
    if user_params['outList'] == '': 
        user_params['outList'] = './full-corpus.csv'
    if user_params['rawDir']  == '': 
        user_params['rawDir'] = './rawdata/'

    return user_params


def dump_user_params( user_params ):

    # dump user params for confirmation
    print 'Input:    '   + user_params['inList']
    print 'Output:   '   + user_params['outList']
    print 'Raw data: '   + user_params['rawDir']
    return


def read_total_list( in_filename ):

    # read total fetch list csv
    fp = open( in_filename, 'rb' )
    reader = csv.reader( fp, delimiter=',', quotechar='"' )

    total_list = []
    for row in reader:
        total_list.append( row )

    return total_list


def purge_already_fetched( fetch_list, raw_dir ):

    # list of tweet ids that still need downloading
    rem_list = []

    # check each tweet to see if we have it
    for item in fetch_list:

        # check if json file exists
        tweet_file = raw_dir + item[2] + '.json'
        if os.path.exists( tweet_file ):

            # attempt to parse json file
            try:
                parse_tweet_json( tweet_file )
                print '--> already downloaded #' + item[2]
            except RuntimeError:
                rem_list.append( item )
        else:
            rem_list.append( item )

    return rem_list


def get_time_left_str( cur_idx, fetch_list, download_pause ):

    tweets_left = len(fetch_list) - cur_idx
    total_seconds = tweets_left * download_pause

    str_hr = int( total_seconds / 3600 )
    str_min = int((total_seconds - str_hr*3600) / 60)
    str_sec = total_seconds - str_hr*3600 - str_min*60

    return '%dh %dm %ds' % (str_hr, str_min, str_sec)

def pull_data(id, raw_dir) :
  
    # Set the API endpoint 
    url = "https://api.twitter.com/1.1/statuses/show/" + id + ".json"

    # Set the base oauth_* parameters along with any other parameters required
    # for the API call.
    params = {
	'oauth_version': "1.0",
	'oauth_nonce': oauth.generate_nonce(),
	'oauth_timestamp': int(time.time())
    }

    # Set up instances of our Token and Consumer. 
    # These keys are given to you by the API provider.
    
    token = oauth.Token(key= TOKEN_KEY, secret= TOKEN_SECRET)
    consumer = oauth.Consumer(key= CONSUMER_KEY, secret= CONSUMER_SECRET)
    client = oauth.Client(consumer)

    # Set our token/key parameters
    params['oauth_token'] = token.key
    params['oauth_consumer_key'] = consumer.key

    # Create our request.
    req = oauth.Request(method="GET", url=url, parameters=params)

    # Sign the request.
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token) 

    # catching json response in resp, data in sdata(string)
    resp, sdata = client.request(req.url)
    
    # converting string data into dictionary
    data = json.loads(sdata)
    
    # writing each response as a .json file
    with open(raw_dir + id + '.json', 'wb') as outfile:
      json.dump(data, outfile, indent=1, separators = (',',':'))
   
    return


def download_tweets( fetch_list, raw_dir ):

    # ensure raw data directory exists
    if not os.path.exists( raw_dir ):
        os.mkdir( raw_dir )

    # stay within rate limits
    max_tweets_per_hr  = 125
    download_pause_sec = 3600 / max_tweets_per_hr

    # download tweets
    for idx in range(0,len(fetch_list)):

        # current item
        item = fetch_list[idx]

        # print status
        trem = get_time_left_str( idx, fetch_list, download_pause_sec )
        print '--> downloading tweet #%s (%d of %d) (%s left)' % \
              (item[2], idx+1, len(fetch_list), trem)

        # pull data
        pull_data(item[2], raw_dir)
	
        # stay in Twitter API rate limits 
        print '    pausing %d sec to obey Twitter API rate limits' % \
              (download_pause_sec)
        time.sleep( download_pause_sec )

    return


def parse_tweet_json( filename ):
    
    # read tweet
    print 'opening: ' + filename
    fp = open( filename, 'rb' )

    # parse json
    try:
        tweet_json = json.load( fp )
    except ValueError:
        raise RuntimeError('error parsing json')

    # look for twitter api error msgs
    if 'errors' in tweet_json:
        raise RuntimeError('error in downloaded tweet')

    # extract creation date and tweet text
    return [ tweet_json['created_at'], tweet_json['text'] ]
    

def build_output_corpus( out_filename, raw_dir, total_list ):

    # open csv output file
    fp = open( out_filename, 'wb' )
    writer = csv.writer( fp, delimiter=',', quotechar='"', escapechar='\\',
                         quoting=csv.QUOTE_ALL )

    # write header row
    writer.writerow( ['Topic','Sentiment','TweetId','TweetDate','TweetText'] )

    # parse all downloaded tweets
    missing_count = 0
    for item in total_list:

        # ensure tweet exists
        if os.path.exists( raw_dir + item[2] + '.json' ):

            try: 
                # parse tweet
                parsed_tweet = parse_tweet_json( raw_dir + item[2] + '.json' )
                full_row = item + parsed_tweet
    
                # character encoding for output
                for i in range(0,len(full_row)):
                    full_row[i] = full_row[i].encode("utf-8")
    
                # write csv row
                writer.writerow( full_row )

            except RuntimeError:
                print '--> bad data in tweet #' + item[2]
                missing_count += 1

        else:
            print '--> missing tweet #' + item[2]
            missing_count += 1

    # indicate success
    if missing_count == 0:
        print '\nSuccessfully downloaded corpus!'
        print 'Output in: ' + out_filename + '\n'
    else: 
        print '\nMissing %d of %d tweets!' % (missing_count, len(total_list))
        print 'Partial output in: ' + out_filename + '\n'

    return


def main():

    check_if_keys_provided()

    # get user parameters
    user_params = get_user_params()
    dump_user_params( user_params )

    # get fetch list
    total_list = read_total_list( user_params['inList'] )
    fetch_list = purge_already_fetched( total_list, user_params['rawDir'] )

    # start fetching data from twitter
    download_tweets( fetch_list, user_params['rawDir'] )

    # second pass for any failed downloads
    print '\nStarting second pass to retry any failed downloads';
    fetch_list = purge_already_fetched( total_list, user_params['rawDir'] )
    download_tweets( fetch_list, user_params['rawDir'] )

    # build output corpus
    build_output_corpus( user_params['outList'], user_params['rawDir'], 
                         total_list )

    return


if __name__ == '__main__':
    main()

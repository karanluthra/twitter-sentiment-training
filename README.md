twitter-sentiment-training
==========================

Training set of 5513 hand-classified tweets for sentiment classifiers

----

This is an upgrade to the original script by Niek J. Sanders available [here] (http://www.sananalytics.com/lab/twitter-sentiment/). 
Twitter's [REST API v1.1] (https://dev.twitter.com/docs/api/1.1) has made it mandatory for all requests to be authenticated using [oauth](https://dev.twitter.com/docs/auth/oauth#v1-1) and hence the script required to incorporate the authentication capability.

Consequently, you must get an access token, access key, consumer token, consumer key by registering your application with twitter, in order to make such authenticated requests. Refer to [this](https://dev.twitter.com/docs/auth/tokens-devtwittercom) guide for getting these tokens, and provide them as global variables in the `install.py` script.

*It is advised to go through the original Readme file given [here](http://www.sananalytics.com/lab/twitter-sentiment/sanders-twitter-0.2.zip) for a better understanding of the project and the install script in particular.*

### Installation
Because of restrictions in Twitter’s Terms of Service, the actual tweets can not be distributed
with the sentiment corpus. A small Python script is included to download all of the tweets. Due
to limitations in Twitter’s API, the download process takes about 43 hours.

Just four easy steps:  
1. Set your access key and secret, consumer key and secret to the global variables declared at the beginning of install.py  
2. Start the tweet downloader script: `python install.py`  
3. Hit enter three times to accept the defaults.  
4. Wait till the script indicates that it’s done.  

Note: the script is smart enough to resume where it left off if downloading is interrupted.
The completed corpus will be in full-corpus.csv. A copy of all the raw data downloaded from Twitter is kept in rawdata/.

----

### Credits
The original work by Niek J. Sanders is a Twitter Sentiment Classifier which can be found [here] (http://www.sananalytics.com/lab/twitter-sentiment/). 
My work is just a little modification to the code written in 2011 to comply with the latest Twitter API v1.1 requirements.

### Support
You may write to me for any help, I'll try and help you to the best of my capability.

Karan Luthra 
karanluthra06@gmail.com



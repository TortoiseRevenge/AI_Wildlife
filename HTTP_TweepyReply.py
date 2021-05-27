#{
#  "AccessToken": "TWITTER_ACCESS_TOKEN_KEY",
#  "AccessTokenSecret": "TWITTER_ACCESS_TOKEN_SECRET_KEY",
#  "ConsumerKey": "TWITTER_CONSUMER_KEY",
#  "ConsumerSecret": "TWITTER_CONSUMER_SECRET_KEY",
#  "id": "@{triggerBody()?['TweetId']}",
#  "text": "We believe that is the @{items('For_each_3')?['species_common']}, of the family  @{items('For_each_3')?['family_common']}. We have a @{items('For_each_3')?['confidence']} % confidence",
#  "username": "@{triggerBody()?['UserDetails']?['UserName']}"
#}

import tweepy
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Begun Function')
    try:
        req_body = req.get_json()
        id = req_body.get('id')
        username = req_body.get('username')
        text = req_body.get('text')
    except:
        return func.HttpResponse("Needs more Data in body")
    try:
        auth = tweepy.OAuthHandler(req_body.get('ConsumerKey'), req_body.get('ConsumerSecret'))
        auth.set_access_token(req_body.get('AccessToken'), req_body.get('AccessTokenSecret'))
        api = tweepy.API(auth)
        logging.info("Preparing to Send")
        api.update_status(f"@{username} {text}", in_reply_to_status_id = id)
        return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
        )
    except:
        return func.HttpResponse("Failed To Post")

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

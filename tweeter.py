import time

import tweepy

from cssbot import take_screenshot
from keys import KEY, SECRET, TOKEN_KEY, TOKEN_SECRET


auth = tweepy.OAuthHandler(KEY, SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

api = tweepy.API(auth)

last_id = api.mentions_timeline(count=1)[0].id


while True:
    mentions = api.mentions_timeline(last_id, tweet_mode="extended")
    for mention in reversed(mentions):
        if mention.is_quote_status:
            continue

        requested_styles = mention.full_text.replace("@scssbot", "")
        image_filename = take_screenshot(requested_styles)
        try:
            image_media = api.media_upload(image_filename)
        except:
            api.update_status(
                "Sorry, we couldn't render your SCSS code 😔",
                in_reply_to_status_id=mention.id,
                auto_populate_reply_metadata=True,
            )
        else:
            api.update_status(
                "Here's your rendered SCSS!",
                in_reply_to_status_id=mention.id,
                auto_populate_reply_metadata=True,
                media_ids=[image_media.media_id],
            )

        last_id = mention.id
    time.sleep(5)

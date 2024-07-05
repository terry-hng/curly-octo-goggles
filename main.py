from investpy import news
import requests
import datetime as dt
import pytz
import os

def there_is_news_incoming(news_list):
    for news in news_list:
        if dt.datetime.strptime(news["time"], time_format) - dt.datetime.strptime(
            dt.datetime.now().strftime(time_format), time_format
        ) <= dt.timedelta(hours=1):
            return True


discord_channel_url = "https://discord.com/api/v9/channels/1258699001268666390/messages"
headers = {
    "Authorization": os.environ.get("DISCORD_AUTH_KEY")
}  # auth key needed to send messages through discord

df = news.economic_calendar(
    time_zone="GMT",
    importances=["high"],
    countries=[
        "united states",
        "new zealand",
        "australia",
        "euro zone",
        "united kingdom",
        "china",
    ],
)

news_list = df[["time", "zone", "event"]].to_dict(orient="records")

# pprint.pprint(news_list)

flags_emoji_dict = {
    "new zealand": "🇳🇿",
    "australia": "🇦🇺",
    "united states": "🇺🇸",
    "china": "🇨🇳",
    "euro zone": "🇪🇺",
    "united kingdom": "🇬🇧",
}

time_format = "%H:%M"

if there_is_news_incoming(news_list=news_list):
    message = "> **Incoming News ⭐⭐⭐**\n\n"

    for news in news_list:
        if (
            dt.timedelta(hours=0)
            <= dt.datetime.strptime(news["time"], time_format)
            - dt.datetime.strptime(dt.datetime.now().strftime(time_format), time_format)
            <= dt.timedelta(hours=1)
        ):
            # print(
            #     dt.datetime.strptime(news["time"], time_format)
            #     - dt.datetime.strptime(
            #         dt.datetime.now().strftime(time_format), time_format
            #     )
            # )

            message += f"{dt.datetime.strptime(news["time"], "%H:%M").replace(tzinfo=pytz.utc).astimezone(dt.timezone(dt.timedelta(hours=7))).strftime("%H:%M")}\t|\t{news["zone"].title()}    {flags_emoji_dict[news["zone"]]}\t|\t**{news["event"]}**\n\n"

    payload = {"content": message + "---------------------------------\n"}

    requests.post(discord_channel_url, payload, headers=headers)

print(message)

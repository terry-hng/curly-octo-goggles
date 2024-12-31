from investpy import news
import requests
import datetime as dt
import pytz
import os

# from pprint import pprint


def convert_to_vietnam_time_object(time_str):
    return pytz.timezone("Asia/Ho_Chi_Minh").localize(
        dt.datetime.strptime(time_str, "%H:%M")
    )


def there_is_news_incoming(news_list):
    for news in news_list:
        if (
            dt.timedelta(hours=0)
            <= convert_to_vietnam_time_object(news["time"])
            - convert_to_vietnam_time_object(
                dt.datetime.strftime(
                    dt.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")), time_format
                )
            )
            <= dt.timedelta(hours=1)
        ):
            return True


discord_channel_url = "https://discord.com/api/v9/channels/1258699001268666390/messages"
headers = {
    "Authorization": os.environ.get("DISCORD_AUTH_KEY")
}  # auth key needed to send messages through discord

df = news.economic_calendar(
    time_zone="GMT +7:00",
    importances=["high"],
    countries=[
        "united states",
        "new zealand",
        "australia",
        "euro zone",
        "united kingdom",
        "china",
        "germany",
    ],
)

if not df.empty:
    news_list = df[["time", "zone", "event", "currency"]].to_dict(orient="records")
    # pprint(news_list)

    flags_emoji_dict = {
        "new zealand": "🇳🇿",
        "australia": "🇦🇺",
        "united states": "🇺🇸",
        "china": "🇨🇳",
        "euro zone": "🇪🇺",
        "united kingdom": "🇬🇧",
        "germany": "🇩🇪",
    }

    time_format = "%H:%M"

    if there_is_news_incoming(news_list=news_list):
        message = "> **Incoming News   ⭐⭐⭐**\n\n"

        for news in news_list:
            if news["time"] != "All Day":
                if (
                    dt.timedelta(hours=0)
                    <= convert_to_vietnam_time_object(news["time"])
                    - convert_to_vietnam_time_object(
                        dt.datetime.strftime(
                            dt.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")),
                            time_format,
                        )
                    )
                    <= dt.timedelta(hours=1)
                ):

                    message += f"- {news["time"]}\t|\t{flags_emoji_dict[news["zone"]]}  {news["zone"].title()} (**{news["currency"]}**)\t|\t**{news["event"]}**\n\n"
            else:
                continue

        payload = {"content": message + "---------------------------------\n"}

        requests.post(discord_channel_url, payload, headers=headers)

        print(message)
    else:
        # for news in news_list:

        #     print(convert_to_vietnam_time_object(news["time"]) - convert_to_vietnam_time_object(dt.datetime.strftime(dt.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")), time_format)))

        print("\nNo News")

# Hertz Freerider Notification System
This tool allows you to track new rides published on hertzfreerider.se, letting you grab them as they appear.
New rides will be sent to you via Telegram through your bot.

# Usage
Set environment variables for your Telegram bot token and your Telegram chat ID. These are stored in TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID, respectively.

Run the script by using:
```console
python hertz.py --from-locations "Malmö" "Lund" "Hässleholm" --to "Stockholm" "Göteborg"
```

This will find any routes from Malmö/Lund/Hässleholm to Stockholm/Göteborg, refreshing every 10 seconds.

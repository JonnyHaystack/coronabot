from datetime import datetime
import logging
from json.decoder import JSONDecodeError

from flag import flagize
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Updater

from coronabot import data
from coronabot import formatting
from coronabot import settings


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Running")


def cbstats(update, context):
    chat_id = update.message.chat_id
    message = ""
    try:
        if len(context.args) == 0:
            stats, updated = data.get_global_cases()
            message = "*Global stats* "
        else:
            country = " ".join(context.args)
            stats, country_info, updated = data.get_country_cases(country)
            message = flagize(
                f":{country_info['country_code']}: "
                f"*{country_info['country_name']}* "
            )
        last_updated = datetime.fromtimestamp(int(updated) / 1000).strftime(
            "%Y-%m-%d %H:%M"
        )
        message += f"({last_updated})\n"
        message += formatting.format_stats(stats)
    except JSONDecodeError:
        if country is not None:
            message = f"{country} doesn't exist lmao"
        else:
            message = "Error: Could not look up stats"
    context.bot.send_message(
        chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN
    )


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    log = logging.getLogger(__name__)

    updater = Updater(settings.TELEGRAM_TOKEN, use_context=True)

    # Set up command handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        CommandHandler("cbstats", cbstats, pass_args=True)
    )

    updater.start_polling()
    updater.idle()

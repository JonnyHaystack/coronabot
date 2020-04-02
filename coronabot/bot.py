import logging
from json.decoder import JSONDecodeError

from flag import flagize
from pycountry import countries
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Updater

from coronabot import data
from coronabot import settings


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Running")


def cbstats(update, context):
    chat_id = update.message.chat_id
    message = ""
    if len(context.args) == 0:
        stats = data.get_global_cases()
        message = (
            "*Global stats*\n"
            f"Confirmed: *{stats['cases']}*\n"
            f"Deaths: *{stats['deaths']}*\n"
            f"Recovered: *{stats['recovered']}*\n"
        )
    else:
        country = " ".join(context.args)
        try:
            stats = data.get_country_cases(country)
            try:
                country_code = countries.lookup(country).alpha_2.lower()
                message = flagize(f":{country_code}: ")
            except LookupError:
                pass
            message += (
                f"*{country}*\n"
                f"Confirmed: *{stats['cases']}* (+{stats['todayCases']})\n"
                f"Current: *{stats['active']}*\n"
                f"Deaths: *{stats['deaths']}* (+{stats['todayDeaths']})\n"
                f"Recovered: *{stats['recovered']}*\n"
            )
        except JSONDecodeError:
            message = f"{country} doesn't exist lmao"
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

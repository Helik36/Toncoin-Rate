import datetime
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


from config.config import BOT_API, ID_CHANNEL
from APICoinMarket import CoinMarket

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def send_message_to_channel(context: ContextTypes.DEFAULT_TYPE):

    coin = CoinMarket()
    current_price_rub = coin.get_data()["price"]["RUB"]
    current_price_uds = coin.get_data()["price"]["USD"]
    percent_change_1h = coin.get_data()["percent_change_1h"]["RUB"]
    percent_change_24h = coin.get_data()["percent_change_24h"]["RUB"]

    text_message = f"{current_price_rub} | {current_price_uds} | 1h: {percent_change_1h}\n24h: {percent_change_24h}"

    await context.bot.send_message(chat_id=context.job.chat_id, text=text_message)

async def start_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_repeating(send_message_to_channel,first=datetime.time(second=10), interval=30, chat_id=ID_CHANNEL)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_API).build()

    application.add_handler(CommandHandler('start_channel', start_channel))

    application.run_polling()

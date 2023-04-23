import logging
from telegram import LabeledPrice, Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Application,CommandHandler,ContextTypes,MessageHandler,PreCheckoutQueryHandler,CallbackQueryHandler,filters)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
PAYMENT_PROVIDER_TOKEN = "381764678:TEST:55033"

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("💰Аҧарашәара")],
        [KeyboardButton("👥 Ҳазҭагылоу")],
        [KeyboardButton("📚Азҵаарақәа")],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    
    await update.message.reply_text("Бзиала шәаабеит!", reply_markup=reply_markup)


async def start_donate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    title = "Агәыҳалалра аарҧшра"
    description = "Афильмқәа реиҭагареи абжьырхаҵареи адгылара аҭаразы аҧарашәара (агәыҳалалра аарҧшра)."
    payload = "Custom-Payload"
    currency = "RUB"
    prices = [
        LabeledPrice("Агәыҳалалразы иахшәаатәуп (100 мааҭк)", 10000),
        LabeledPrice("Агәыҳалалразы иахшәаатәуп (200 мааҭк)", 20000),
        LabeledPrice("Агәыҳалалразы иахшәаатәуп (500 мааҭк)", 50000)
    ]

    buttons = []
    for price in prices:
        button = InlineKeyboardButton(
            f"{price.label}",
            callback_data=f"donate_{price.amount}"
        )
        buttons.append([button])
    
    keyboard = InlineKeyboardMarkup(buttons)
    
    message = "Афильмқәа реиҭагареи абжьырхаҵареи адгылара аҭаразы аҧарашәара (агәыҳалалра аарҧшра)."
    await context.bot.send_message(chat_id, message, reply_markup=keyboard)


async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id

    try:
        price = int(query.data.split("_")[1])
    except (IndexError, ValueError):
        await query.answer("Invalid selection")
        return

    title = "Агәыҳалалра аарҧшра"
    description = "Афильмқәа реиҭагареи абжьырхаҵареи адгылара аҭаразы аҧарашәара (агәыҳалалра аарҧшра)."
    payload = "Custom-Payload"
    currency = "RUB"
    prices = [
        LabeledPrice("Агәыҳалалразы иахшәаатәуп (100 мааҭк)", 10000),
        LabeledPrice("Агәыҳалалразы иахшәаатәуп (200 мааҭк)", 20000),
        LabeledPrice("Агәыҳалалразы иахшәаатәуп (500 мааҭк)", 50000)
    ]
    index = 0
    for i, obj in enumerate(prices):
        if obj["amount"] == price:
            index = i
    if price in [p.amount for p in prices]:
        await context.bot.send_invoice(
            chat_id, title, description, payload,
            PAYMENT_PROVIDER_TOKEN, currency, [prices[index]],
            provider_data={"price": price}
        )
    else:
        await query.answer("Invalid selection")

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    if query.invoice_payload != "Custom-Payload":
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Иҭабуп иаашәырҧшыз агәыҳалалразы!")


def main() -> None:
    application = Application.builder().token("").build()
    application.add_handler(CommandHandler("start", start_callback))
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.Regex("^(💰Аҧарашәара)$"), start_donate_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    application.run_polling()


if __name__ == "__main__":
    main()

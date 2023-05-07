import requests
import sqlite3
import logging
from telegram import LabeledPrice, Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (Application,CommandHandler,ContextTypes,MessageHandler,PreCheckoutQueryHandler,CallbackQueryHandler,filters)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
PAYMENT_PROVIDER_TOKEN = ""
BOT_TOKEN = "6122399712:AAHdUGZ-1Cv822Tdu_69Hjt6CMXNFPmbkBA"

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
    description = "Афильмқәа реиҭагареи абжьырхаҵареи адгылара аҭаразы аҧарашәара (агәыҳалалра аарҧшра).\nАгәыҳалалразы иахшәаатәуп:"
    payload = "Custom-Payload"
    currency = "RUB"
    prices = [
        LabeledPrice("100 мааҭ", 10000),
        LabeledPrice("200 мааҭ", 20000),
        LabeledPrice("500 мааҭ", 50000),
        LabeledPrice("1000 мааҭ", 100000)
    ]

    buttons = [
        [
            InlineKeyboardButton(f"{prices[0].label}",callback_data=f"donate_{prices[0].amount}"),
            InlineKeyboardButton(f"{prices[1].label}",callback_data=f"donate_{prices[1].amount}"),
        ],
        [
            InlineKeyboardButton(f"{prices[2].label}",callback_data=f"donate_{prices[2].amount}"),
            InlineKeyboardButton(f"{prices[3].label}",callback_data=f"donate_{prices[3].amount}"),
        ],
    ]
    
    keyboard = InlineKeyboardMarkup(buttons)
    
    message = "Афильмқәа реиҭагареи абжьырхаҵареи адгылара аҭаразы аҧарашәара (агәыҳалалра аарҧшра).\nАгәыҳалалразы иахшәаатәуп:"
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
    description = "Афильмқәа реиҭагареи абжьырхаҵареи адгылара аҭаразы аҧарашәара (агәыҳалалра аарҧшра).\nАгәыҳалалразы иахшәаатәуп:"
    payload = "Custom-Payload"
    currency = "RUB"
    prices = [
        LabeledPrice("100 мааҭ", 10000),
        LabeledPrice("200 мааҭ", 20000),
        LabeledPrice("500 мааҭ", 50000),
        LabeledPrice("1000 мааҭ", 100000)
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
    # Save the amount to the database
    amount = update.message.successful_payment.total_amount/100
    conn = sqlite3.connect('contributions.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS contributions (user_id INTEGER, amount REAL)")
    c.execute("INSERT INTO contributions VALUES (?, ?)", (update.effective_user.id, amount))
    conn.commit()
    conn.close()

    # Define the callback function for the /total command
async def total_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conn = sqlite3.connect('contributions.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS contributions (user_id INTEGER, amount REAL)")
    user_total = c.execute("SELECT SUM(amount) FROM contributions WHERE user_id=?", (update.effective_user.id,)).fetchone()[0]
    all_total = c.execute("SELECT SUM(amount) FROM contributions").fetchone()[0]
    conn.close()
    
    if user_total == None:
        user_total = 0
    if all_total == None:
        all_total = 0
    # Send the user's contribution total and the total amount contributed by all users
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Адонорцәа рзеиҧш лагала:\n{} мааҭ\n\nУара узеиҧш лагала:\n{} мааҭ".format(user_total, all_total))

    # Define the callback function for the /crypto command
async def crypto_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Make API requests for ticker data
    binance_url = 'https://api.binance.com/api/v3/ticker/price'
    okex_url = 'https://www.okex.com/api/v5/market/tickers?instType=SPOT'
    binance_response = requests.get(binance_url)
    okex_response = requests.get(okex_url)
    binance_data = binance_response.json()
    okex_data = okex_response.json()

    # Create a dictionary to store the prices of each trading pair
    prices = {}
    for ticker in binance_data:
        symbol = ticker['symbol']
        price = float(ticker['price'])
        prices[symbol] = {'binance': price}
    for ticker in okex_data['data']:
        symbol = ticker['instId'].replace('-', '')
        price = float(ticker['last'])
        if symbol in prices:
          prices[symbol]['okex'] = price

    # Iterate over all possible pairs and find profitable spreads
    text = ""
    for pair in prices.keys():
        if 'okex' in prices[pair] and 'binance' in prices[pair]:
            okex_price = prices[pair]['okex']
            binance_price = prices[pair]['binance']
            spread = abs(round(okex_price - binance_price, 2))
            if spread > 1:
               text += pair+": OKEx = "+str(okex_price)+", Binance = "+str(binance_price)+", spread = "+str(spread)+"\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_callback))
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.Regex("^(💰Аҧарашәара)$"), start_donate_callback))
    application.add_handler(MessageHandler(filters.Regex("^(👥 Ҳазҭагылоу)$"), total_callback))
    application.add_handler(MessageHandler(filters.Regex("^(📚Азҵаарақәа)$"), crypto_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    application.run_polling()


if __name__ == "__main__":
    main()

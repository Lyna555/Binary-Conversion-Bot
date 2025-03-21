from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import nest_asyncio

nest_asyncio.apply()

# 🔹 Bot Credentials
BOT_TOKEN = "7871315204:AAHw3uV0qAUbT8dKEHi-aajS3Qfod5Yuqg0"

# Define keyboard buttons
reply_keyboard = [
    ["Binary to Decimal", "Decimal to Binary"]
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Please choose a conversion type:", reply_markup=markup)

async def convert(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()

    if text == "Binary to Decimal":
        await update.message.reply_text("Enter a binary number (only 0s and 1s):")
        context.user_data["conversion"] = "bin_to_dec"

    elif text == "Decimal to Binary":
        await update.message.reply_text("Enter a decimal number:")
        context.user_data["conversion"] = "dec_to_bin"

    elif "conversion" in context.user_data:
        conversion_type = context.user_data["conversion"]

        if conversion_type == "bin_to_dec":
            if all(c in '01' for c in text):
                decimal_value = int(text, 2)
                await update.message.reply_text(f"Binary {text} = Decimal {decimal_value}")
            else:
                await update.message.reply_text("Invalid binary number! Please enter only 0s and 1s.")

        elif conversion_type == "dec_to_bin":
            if text.isdigit():
                binary_value = bin(int(text))[2:]
                await update.message.reply_text(f"Decimal {text} = Binary {binary_value}")
            else:
                await update.message.reply_text("Invalid decimal number! Please enter a valid number.")

        context.user_data.pop("conversion")  # Reset choice after conversion

    else:
        await update.message.reply_text("Please select a conversion type first.", reply_markup=markup)

def app():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert))

    print("Bot is running...")
    app.run_polling()

asyncio.get_event_loop().run_until_complete(app())


# 🔹 Telethon API Credentials
# API_ID = 25583057
# API_HASH = "ddb961b411d90234af0e7adc10f17031"

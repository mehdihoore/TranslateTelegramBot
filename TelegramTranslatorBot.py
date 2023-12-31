import logging
import tempfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

translator = Translator()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("درود! متن را ارسال کنید تا آن را به انگلیسی و فارسی ترجمه کنم. در صورت طولانی بودن متن هر پیام ارسالی در قالب یک فایل html نیز نمایش داده می شود.")
def translate_and_send_messages(update: Update, messages: list) -> None:
    for message in messages:
        update.message.reply_text(message, parse_mode='HTML')

def translate_text(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    translation_en = translator.translate(text, src='auto', dest='en').text
    translation_fa = translator.translate(text, src='auto', dest='fa').text

    # Create translated messages
    response_en = f"English Translation: {translation_en}"
    response_fa = f"ترجمه فارسی: {translation_fa}"

    # Calculate maximum characters per message
    max_chars_per_message = 4096  # Telegram message limit

    # Split translated messages into chunks that fit within Telegram's limit
    response_en_chunks = [response_en[i:i + max_chars_per_message] for i in range(0, len(response_en), max_chars_per_message)]
    response_fa_chunks = [response_fa[i:i + max_chars_per_message] for i in range(0, len(response_fa), max_chars_per_message)]

    # Create an HTML content with styling
    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    background-color: #f5f5f5;
                    font-family: Arial, sans-serif;
                }}
                .quote-en {{
                    border-left: 4px solid #3498db;
                    margin: 10px;
                    padding: 10px;
                    background-color: #ffffff;
                    direction: ltr;
                }}
                .quote-fa {{
                    border-left: 4px solid #e74c3c;
                    margin: 10px;
                    padding: 10px;
                    background-color: #f9ebae;
                    direction: rtl;
                    font-family: Tahoma, Arial, sans-serif;
                }}
            </style>
        </head>
        <body>
            <div class="quote-en">
                <p><strong>English Translation:</strong></p>
                <p>{translation_en}</p>
            </div>
            <div class="quote-fa">
                <p><strong>ترجمه فارسی:</strong></p>
                <p>{translation_fa}</p>
            </div>
        </body>
    </html>
    """

    if len(html_content) <= 2096:
        response = f"English Translation: {translation_en}\nترجمه فارسی: {translation_fa}"
        update.message.reply_text(response, parse_mode='HTML')
    else:
        response ="میتوانید ترجمه را در قالب یک فایل نیز مشاهده کنید"

        # Save the long message to an HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_file:
            temp_file.write(html_content)
            temp_file_path = temp_file.name

        # Send the HTML file
        with open(temp_file_path, 'rb') as temp_file:
            update.message.reply_document(temp_file, caption='Translations.html', parse_mode='HTML')
        update.message.reply_text(response, parse_mode='HTML')

    # Send translated messages in chunks
    translate_and_send_messages(update, response_en_chunks)
    translate_and_send_messages(update, response_fa_chunks)

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send an error message to the user."""
    logging.error(f"Error occurred: {context.error}")
    update.message.reply_text("An error occurred while processing your request. Please try again later.")

def main():
    start_handler = CommandHandler('start', start)
    translate_handler = MessageHandler(Filters.text & ~Filters.command, translate_text)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(translate_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

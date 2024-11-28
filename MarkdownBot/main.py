import markdown2
import telebot
import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext


API_TOKEN = "7395755630:AAEeLFEYNAovV9V7nE7mvw_OHEJQvZkyzig"

bot = telebot.TeleBot(API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# Define a command handler
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to YourBot! Type /info to get more information.")

@bot.message_handler(commands=["info"])
def send_info(message):
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")


def escape_markdown_v2(text):
    """Escape only MarkdownV2 special characters outside Markdown entities."""
    escape_chars = r"_*[]()~>#+-=|{}.!"
    return ''.join(f"\\{char}" if char in escape_chars else char for char in text)

@bot.message_handler(commands=["syntax"])
def send_syntax(message):
    cheatsheet = (
        "*MarkdownV2 Syntax Cheatsheet:*\n\n"
        "*bold*: `**text**`\n"
        "_italic_: `_text_`\n"
        "__underline__: `__text__`\n"
        "~strikethrough~: `~text~`\n"
        # "||spoiler||: `||text||`\n\n"
        "[Links]\\(http://example\\.com\\): Use `[text]\\(URL\\)`\n"
        "Example: \\[Click Here\\]\\(http://example\\.com\\)\n\n"
        "`Inline Code`: Use \\`text\\`\n"
        "Code Block: Use triple backticks \\[\\`\\`\\`\\] to encase the text  \n"
        "```\n"
        "print\\('Hello, World!'\\)\n"
        "```"
    )


    bot.reply_to(message, cheatsheet, parse_mode="MarkdownV2")


@bot.message_handler(commands=["bold"])
def send_bold(message):
    user_input = (message.text)
    command, separator, text = user_input.partition("bold")

    if not user_input.strip():
        bot.reply_to(message, "Please provide text to make bold.")
        return

    escaped_text = escape_markdown_v2(text.strip())  # Clean up whitespace
    bold_text = f"`**{escaped_text.strip()}**`"
    bot.reply_to(message, bold_text, parse_mode="MarkdownV2")


@bot.message_handler(commands=["italic"])
def send_italic(message):
    user_input = (message.text)
    command, separator, text = user_input.partition("italic")

    if not user_input.strip():
        bot.reply_to(message, "Please provide text to make italic.")
        return

    escaped_text = escape_markdown_v2(text.strip())  # Clean up whitespace
    italic_text = f"`_{escaped_text.strip()}_`"
    bot.reply_to(message, italic_text, parse_mode="MarkdownV2")


quiz_questions = [
    {
        "question": "Which syntax is used to bold text in Markdown?",
        "options": ["**text**", "_text_", "`text`", "~~text~~"],
        "answer": "A"  # Correct option
    },
    {
        "question": "How do you create a hyperlink in Markdown?",
        "options": [
            "[Link](http://example.com)",
            "<a href='http://example.com'>Link</a>",
            "http://example.com",
            "Link: example.com"
        ],
        "answer": "A"
    }
]

@bot.message_handler(commands=["mcq"])
def start_mcq(message):
    user_id = message.from_user.id
    user_progress[user_id] = 0  # Start the first question
    send_mcq_question(message, user_id)



# def handle_messages(messages):
# 	for message in messages:
# 		# Do something with the message
# 		bot.reply_to(message, 'Hi')

# bot.set_update_listener(handle_messages)
# Start the bot
bot.polling()
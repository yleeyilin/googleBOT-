import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import requests
import string
from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup


# Set up the Telegram bot using your bot's access token
Token = ${{secrets.TOKEN}}
updater = Updater(Token, use_context = True)
dispatcher= updater.dispatcher

# Set up ChatGPT using your OpenAI API key
# openai.api_key = ${{secrets.TOKEN}}

# Define the function to generate a response using ChatGPT
def start(update, context):
    update.message.reply_text("Hi there, use me to search about a topic!")

# Define a function to generate responses
def generate_response(query, index):
    fallback = "Sorry, I cannot think of a reply for that."
    result = ''

    try:
        search_result_list = list(search(query))

        page = requests.get(search_result_list[index])

        tree = html.fromstring(page.content)

        soup = BeautifulSoup(page.content, features="lxml")

        article_text = ''
        article = soup.findAll('p')
        for element in article:
            article_text += '\n' + ''.join(element.findAll(text = True))
        article_text = article_text.replace('\n', '')
        first_sentence = article_text.split('.')
        first_sentence = first_sentence[0].split('?')[0]

        chars_without_whitespace = first_sentence.translate(
            { ord(c): None for c in string.whitespace }
        )

        if len(chars_without_whitespace) > 0:
            result = first_sentence
        else:
            result = fallback

        return result
    except Exception as e:
    # Catch the exception and print the error message
        print(f"An error occurred: {e}")
    """ except:
        if len(result) == 0: result = fallback
        return result """

""" def generate_response(message):
    if message is None:
        return "Sorry, I didn't catch that. Can you please repeat?"
    prompt = f"Can you tell me more about {message}\n"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip() """

# Define the behavior of the bot when it receives a message
def respond_to_message(update, context):
    message_text = update.message.text
    user_id = update.message.chat_id
    response_text = generate_response(message_text, 0)
    context.bot.send_message(chat_id=user_id, text=response_text)
    
# Run the bot
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, respond_to_message))
updater.start_polling()
updater.idle()

import telebot
import requests
import re
import json


ItemName = ""


bot = telebot.TeleBot("token")



@bot.message_handler(commands=['start'])
def send_welcome(message):
	
	bot.send_message(message.chat.id, "Пиши название предмета")

@bot.message_handler(content_types=['text'])

def send_text(message):

	if len(message.text) < 3:
		bot.send_message(message.chat.id, "Не меньше трех символов.")
	else:
		ItemName = str(message.text)
		headers = {
			'x-api-key': 'your_api_key',
		}

		params = (
			('q', ItemName),
		)

		response = requests.get('https://tarkov-market.com/api/v1/item', headers=headers, params=params)

		responseText = re.sub(',', '\n', response.text)
		try:
			
			data = "\n".join(['Предмет: {name},  мин.цена: {price}'.format(**x) for x in json.loads(response.text)])
			
			bot.send_message(message.chat.id, data)
		except:
			bot.send_message(message.chat.id, "Предмет " + message.text.lower() + " не найден.")
			
bot.polling()
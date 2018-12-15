# -*- coding: utf-8 -*-

#Telegram
import telegram
from telegram.ext import Updater, Filters, MessageHandler

#QR Code
import qrcode
import qrtools

#System libraries
import os
from os import listdir
from os.path import isfile, join

from io import BytesIO
from PIL import Image

TOKEN = "TOKEN_FROM_@BOTFATHER"

def decode(bot, update):
	chat_id = update.message.chat_id

	if update.message.photo:
		id_img = update.message.photo[-1].file_id
	else:
		return

	foto = bot.getFile(id_img)

	new_file = bot.get_file(foto.file_id)
	new_file.download('qrcode.png')

	qr = qrtools.QR()

	try:
		qr.decode("qrcode.png")
		bot.sendMessage(chat_id=chat_id, text=qr.data)
		os.remove("qrcode.png")
	except Exception as e:
		bot.sendMessage(chat_id=chat_id, text=str(e))

def main():
	updater = Updater(TOKEN)
	dp = updater.dispatcher

	dp.add_handler(MessageHandler(Filters.photo, decode))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

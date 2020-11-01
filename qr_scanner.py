# -*- coding: utf-8 -*-

# Telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, Filters, MessageHandler, CallbackContext

# QR Code
from pyzbar.pyzbar import decode

# System libraries
import os
from os import listdir
from os.path import isfile, join

from io import BytesIO
from PIL import Image

TOKEN = "TOKEN_FROM_@BOTFATHER"

def decode_qr(update: Update, context: CallbackContext):
	chat_id = update.message.chat_id

	if update.message.photo:
		id_img = update.message.photo[-1].file_id
	else:
		return

	foto = context.bot.getFile(id_img)

	new_file = context.bot.get_file(foto.file_id)
	new_file.download('qrcode.png')

	try:
		result = decode(Image.open('qrcode.png'))
		context.bot.sendMessage(chat_id=chat_id, text=result[0].data.decode("utf-8"))
		os.remove("qrcode.png")
	except Exception as e:
		context.bot.sendMessage(chat_id=chat_id, text=str(e))

def main():
	updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
	dp = updater.dispatcher

	dp.add_handler(MessageHandler(Filters.photo, decode_qr))

	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()

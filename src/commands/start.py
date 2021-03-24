from telegram import Update
from telegram.ext import CommandHandler
from auth import auth
import logging

def start(update, context):
	if(auth.auth(update, context)):
		context.bot.send_message(chat_id=update.effective_chat.id, text=
	"Ciao! Sono AvenaChessBot e gestirò i Tornei Avenoni Scacchisti.\nUsa /help per visualizzare i 		comandi disponibili.\n")
		logging.info("Replied to message.")
	else:
		pass

handler = CommandHandler('start', start)

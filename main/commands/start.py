from main import auth
from telegram import Update
from telegram.ext import CommandHandler

def start(update, context):
	if(auth.auth(update, context)):
		context.bot.send_message(chat_id=update.effective_chat.id, text=
	"Ciao! Sono AvenaChessBot e gestirò i Tornei Avenoni Scacchisti.\nUsa /help per visualizzare i 		comandi disponibili, oppure usa /torneo per visualizzare informazioni sul torneo.\n")
	else:
		pass

handler = CommandHandler('start', start)

import logging
import operator
import sqlite3
import imgkit
from sqlite3 import Error
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from auth import auth
from commands import start, partecipanti, risultati, classifica

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def execute(conn, command):
	cur = conn.cursor()
	cur.execute(command)
	return cur.fetchall()

def count(conn, table):
	cur = conn.cursor()
	cur.execute("SELECT count(*) FROM " + table)
	return cur.fetchall()[0][0]

def isEmpty(conn, table):
	return (count(conn, table) == 0)



def main() -> None:
	# Create the Updater and pass it your bot's token.
	f = open(".credentials/token.txt", "r")
	updater = Updater(f.readline().strip(), use_context=True)
	f.close()

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher
	dispatcher.add_handler(auth.handler)
	dispatcher.add_handler(start.handler)
	dispatcher.add_handler(partecipanti.handler)
	dispatcher.add_handler(risultati.handler)
	dispatcher.add_handler(classifica.handler)

	# Start the Bot
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()

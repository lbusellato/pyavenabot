from telegram.ext import CommandHandler
from auth import auth
from sql import sql
from utils import utils
import logging


def partite(update, context):
    conn = sql.sql()
    reply=""
    if auth.auth(update, context):
        conn.open(r".db/avenabot.db")
        group = update.message.text[-1]
        if group == "A" or group == "B" or group == "F":
            if not conn.is_empty("girone" + group + "games"):
                game_list = conn.execute("SELECT * FROM girone" + group + "games;")
                reply += "Partite girone " + group + ":"
                for g in game_list:
                    reply += "\n" + utils.get_lichess_id(g[1]) + " vs " + utils.get_lichess_id(g[2]) + ":\n"
                    reply += g[3]
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply, disable_web_page_preview=True)
                conn.close()
                logging.info("Replied to message.")
            else:
                reply = "Non sono ancora state giocate partite nel girone"
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
                conn.close()
                logging.info("Replied to message.")
        else:
            if not conn.is_empty("gironeFgames"):
                reply += "Il gruppo indicato non è valido, prova con: F"
            elif not conn.is_empty("gironeAgames"):
                reply += "Il gruppo indicato non è valido, prova con: A, B"
            else:
                reply += "Non è stata ancora giocata nessuna partita"
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
            conn.close()
            logging.info("Replied to message.")
    else:
        pass


handler = CommandHandler('partite', partite)

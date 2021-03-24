from os.path import dirname, abspath
import sqlite3
from telegram.ext import (
    MessageHandler,
    Filters,
)
import logging


def execute(conn, command):
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()


def exists(conn, table, key):
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table + " WHERE chatID=" + str(key))
    return cur.fetchall()


def auth(update, context):
    chat_id = update.effective_chat.id
    user = update.message.from_user.username
    msg_text = update.message.text
    logging.info("Received message from " + user + " in chat " + str(chat_id) + ": " + msg_text)
    if chat_id > 0:
        d = dirname(dirname(abspath(__file__))) + "/.db/avenabot.db"
        conn = sqlite3.connect(d)
        cur = conn.cursor()
        cur.execute("SELECT * FROM auth WHERE chatID=" + str(chat_id))
        if not cur.fetchall():
            context.bot.send_message(chat_id, text="Non ti conosco, immetti la password per favore:")
            execute(conn, "INSERT INTO auth (chatID, authorized) VALUES (" + str(chat_id) + ",0)")
        else:
            cur.execute("SELECT * FROM auth WHERE chatID=" + str(chat_id))
            if cur.fetchall()[0][2] == 0:
                message = update.message.text
                d = dirname(dirname(abspath(__file__))) + "/.credentials/pwd.txt"
                f = open(d, "r")
                if message != f.readline().strip():
                    context.bot.send_message(chat_id, text="Password incorretta, riprova per favore.")
                else:
                    context.bot.send_message(chat_id,
                                             text="Password corretta, ora puoi utilizzare i comandi liberamente.")
                    execute(conn, "UPDATE auth SET authorized='1' WHERE chatID=" + str(chat_id))
            else:
                conn.close()
                return True
    else:
        return True
    conn.close()
    return False


handler = MessageHandler(Filters.text & (~Filters.command), auth)

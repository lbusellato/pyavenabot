from telegram.ext import CommandHandler
from auth import auth
import logging
from commands import (
    partecipanti,
    risultati,
    classifica,
    partite,
    miepartite,
    iscrivimi,
    inserisci,
)

cmd_list = [partecipanti.cmd, risultati.cmd, classifica.cmd, partecipanti.cmd, partite.cmd, miepartite.cmd, inserisci.cmd, iscrivimi.cmd]

def _help(update, context):
    if auth.auth(update, context):
        message = ""
        for c in cmd_list:
            message += c.name + "\n\n" + c.desc + "\n"
            for i in range(80):
                message += "-"
            message += "\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        logging.info("Replied to message.")
    else:
        pass


handler = CommandHandler('help', _help)

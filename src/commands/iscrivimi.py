from telegram.ext import CommandHandler
from auth import auth
from sql import sql
from utils import utils
import logging


def iscrivimi(update, context):
    conn = sql.sql()
    if auth.auth(update, context):
        conn.open(r".db/avenabot.db")
        if update.message.text == "/iscrivimi":
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Per favore specifica il tuo nickname Lichess dopo il comando /iscrivimi.")
            logging.info("Replied to message.")
        else:
            player_username = update.message.from_user.username
            player_lid = update.message.text[11:]
            if not utils.lid_exists(player_lid):
                if not conn.exists("Partecipanti", "tgid", player_username):
                    utils.insert_player(conn, player_username, player_lid)
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Ti ho iscritto!")
                    logging.info("Replied to message.")
                    conn.close()
                else:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Risulti già iscritto!")
                    logging.info("Replied to message.")
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Il nickname Lichess che hai inserito non sembra esistere!")
                logging.info("Replied to message.")
    else:
        pass

cmd = utils.Command("/iscrivimi LichessID", "Iscrive al torneo.")
handler = CommandHandler('iscrivimi', iscrivimi)

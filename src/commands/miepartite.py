from telegram.ext import CommandHandler
from auth import auth
from sql import sql
from utils import utils
import logging


def miepartite(update, context):
    conn = sql.sql()
    if auth.auth(update, context):
        conn.open(r".db/avenabot.db")
        player_username = update.message.from_user.username
        if update.message.text != "/miepartite" and player_username == "lbusellato":
            msg = update.message.text.replace("/miepartite", " ").strip()
            player_username = msg
        if conn.exists("partecipanti", "tgid", player_username):
            player_group = conn.execute("SELECT gid FROM partecipanti WHERE tgid='" + player_username + "';")[0][0]
            player_tid = conn.execute("SELECT tid FROM partecipanti WHERE tgid='" + player_username + "';")[0][0]
            if not conn.is_empty("girone" + player_group):
                res = utils.get_player_games(player_tid).replace(',', '')
                player_gid = conn.execute("SELECT gid FROM girone" + player_group + " WHERE tid='" + str(player_tid) + "';")[0][0]
                opponent_list = conn.execute("SELECT * FROM girone" + player_group + ";")
                reply = "Devi ancora giocare contro:\n"
                i = 0
                for o in opponent_list:
                    if o[1] != player_tid and res[o[3] - 1] == 'n':
                        reply += utils.get_lichess_id(o[1]) + "(@" + utils.get_tg_id(o[1]) + "), giochi col "
                        if player_gid % 2 == 0:
                            if i % 2 == 0:
                                reply += "bianco.\n"
                            else:
                                reply += "nero.\n"
                        else:
                            if i % 2 == 0:
                                reply += "nero.\n"
                            else:
                                reply += "bianco.\n"
                    if o[1] != player_tid:
                        i += 1
                if reply == "Devi ancora giocare contro:\n":
                    reply = "Hai giocato tutte le tue partite."
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=reply)
                logging.info("Replied to message.")
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Non sono ancora state generate le partite nel tuo girone.")
                logging.info("Replied to message.")
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Non mi sembra che tu sia iscritto al torneo.")
            logging.info("Replied to message.")
    else:
        pass


cmd = utils.Command("/miepartite", "Mostra la lista di partite che devi ancora giocare con il colore che devi usare.")
handler = CommandHandler('miepartite', miepartite)

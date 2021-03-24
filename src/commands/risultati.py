import imgkit
import logging
from telegram.ext import CommandHandler
from auth import auth
from utils import utils
from sql import sql

conn = sql.sql()


def fetch_results(group):
    html = "<div><table border=\"1\" cellspacing=\"0\" cellpadding=\"4\" align=\"center\"><tr><b>Risultati girone "
    html += group
    table = "girone" + group
    html += "<tr><td></td>"
    player_list = conn.execute("SELECT * FROM " + table + ";")
    for p in player_list:
        html += "<td align=\"center\">" + str(p[1]) + "</td>"
    html += "</tr>"
    k = 0
    for p in player_list:
        if k % 2 == 0:
            html += "<tr bgcolor=\"#e9ede4\">"
        else:
            html += "<tr bgcolor=\"#d7edb4\">"
        k += 1
        html += "<td>(" + str(p[1]) + ") " + utils.getLichessID(p[1]) + "</td>"
        for r in p[2]:
            if r != ",":
                html += "<td width=\"20px\" align=\"center\">"
                if r == "d":
                    html += "&#189"
                elif r != "n":
                    html += r
                html += "</td>"
        html += "</tr>"
    html += "</table></div>"
    return html


def risultati(update, context):
    if auth.auth(update, context):
        conn.open(r".db/avenabot.db")
        if conn.is_empty('gironeF'):
            if not conn.is_empty('gironeA'):
                html = fetch_results('A') + fetch_results('B')
                options = {
                    'quiet': '',
                    'width': '600',
                }
                imgkit.from_string(html, 'out.jpg', options=options)
                context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
                logging.info("Replied to message.")
                conn.close()
        else:
            html = fetch_results('F')
            options = {
                'quiet': '',
                'width': '400',
            }
            imgkit.from_string(html, 'out.jpg', options=options)
            context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
            logging.info("Replied to message.")
            conn.close()
            pass
    else:
        pass


handler = CommandHandler('risultati', risultati)

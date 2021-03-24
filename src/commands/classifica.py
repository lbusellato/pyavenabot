import operator
import imgkit
import logging
from telegram.ext import CommandHandler
from auth import auth
from sql import sql
from utils import utils


def classifica(update, context):
    conn = sql.sql()
    if auth.auth(update, context):
        conn.open(r".db/avenabot.db")
        if not conn.is_empty("gironeF"):
            html = "<div>"
            html += "<br><table border=\"1\" cellspacing=\"0\" cellpadding=\"2\" align=\"center\"><tr><b>Classifica girone finale"
            player_list = conn.execute("SELECT * FROM gironeF;")
            res_list = []
            for p in player_list:
                res = [p[1], p[2]]
                tot = 0
                for r in p[2]:
                    if r == "d":
                        tot += 0.5
                    elif r == "1":
                        tot += 1
                res.append(tot)
                res_list.append(res)
            res_list = sorted(res_list, key=operator.itemgetter(2), reverse=True)
            html += "<th>ID</th>"
            for i in range(len(res_list) - 1):
                html += "<th>G" + str(i + 1) + "</th>"
            html += "<th>PTI</th>"
            k = 0
            for p in res_list:
                if k % 2 == 0:
                    html += "<tr bgcolor=\"#e9ede4\"><td>"
                else:
                    html += "<tr bgcolor=\"#d7edb4\"><td>"
                html += utils.get_lichess_id(p[0]) + "</td>"
                k += 1
                j = 0
                for r in p[1]:
                    if r != "," and r != "n" and r != "x":
                        j += 1
                        if r == "d":
                            html += "<td align=\"center\">&#189;</td>"
                        else:
                            html += "<td align=\"center\">" + str(r) + "</td>"
                for i in range(len(res_list) - j - 1):
                    html += "<td> </td>"
                html += "<td align=\"center\">"
                if p[2] % 1 == 0:
                    html += str(int(p[2]))
                else:
                    if int(p[2]) != 0:
                        html += str(int(p[2]))
                    html += "&#189;"
                html += "</td></tr>"
            html += "</table></div>"
            options = {
                'quiet': '',
                'width': '400',
            }
            imgkit.from_string(html, 'out.jpg', options=options)
            context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
            conn.close()
        elif not conn.is_empty("gironeA"):
            html = "<div>"
            for l in range(2):
                html += "<br><table border=\"1\" cellspacing=\"0\" cellpadding=\"2\" align=\"center\"><tr><b>Classifica girone "
                table = ""
                if l == 0:
                    table = "gironeA"
                    html += "A:</b></tr>"
                else:
                    table = "gironeB"
                    html += "B:</b></tr>"
                player_list = conn.execute("SELECT * FROM " + table + ";")
                res_list = []
                for p in player_list:
                    res = [p[1], p[2]]
                    tot = 0
                    for r in p[2]:
                        if r == "d":
                            tot += 0.5
                        elif r == "1":
                            tot += 1
                    res.append(tot)
                    res_list.append(res)
                res_list = sorted(res_list, key=operator.itemgetter(2), reverse=True)
                html += "<th>ID</th>"
                for i in range(len(res_list) - 1):
                    html += "<th>G" + str(i + 1) + "</th>"
                html += "<th>PTI</th>"
                k = 0
                for p in res_list:
                    if k % 2 == 0:
                        html += "<tr bgcolor=\"#e9ede4\"><td>"
                    else:
                        html += "<tr bgcolor=\"#d7edb4\"><td>"
                    html += utils.get_lichess_id(p[0]) + "</td>"
                    k += 1
                    j = 0
                    for r in p[1]:
                        if r != "," and r != "n" and r != "x":
                            j += 1
                            if r == "d":
                                html += "<td align=\"center\">&#189;</td>"
                            else:
                                html += "<td align=\"center\">" + str(r) + "</td>"
                    for i in range(len(res_list) - j - 1):
                        html += "<td> </td>"
                    html += "<td align=\"center\">"
                    if p[2] % 1 == 0:
                        html += str(int(p[2]))
                    else:
                        if int(p[2]) != 0:
                            html += str(int(p[2]))
                        html += "&#189;"
                    html += "</td></tr>"
                html += "</table>"
            html += "</div>"
            options = {
                'quiet': '',
                'width': '400',
            }
            imgkit.from_string(html, 'out.jpg', options=options)
            context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
            logging.info("Replied to message.")
            conn.close()
    else:
        pass


handler = CommandHandler('classifica', classifica)

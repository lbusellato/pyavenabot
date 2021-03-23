from main import auth
from telegram import Update
from telegram.ext import CommandHandler
import imgkit
import sqlite3

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

def partecipanti(update, context):
	if(auth.auth(update, context)):
		conn = sqlite3.connect(r".db/avenabot.db")
		html = '<div><table border="1" cellspacing="0" cellpadding="4" align="center"><tr><th>TID</th><th>ID Lichess</th><th>ID Telegram</th><th>ELO</th>'
		if (not isEmpty(conn, "gironeA")):
		    html += "<th>Girone</th></tr>"
		cur = conn.cursor()
		cur.execute("SELECT * FROM partecipanti")
		#Pull each player's data from the db and nicely format it
		for p in cur.fetchall():
			html += "<tr align>"
			html += "<td align=\"center\">" + str(p[1]) + "</td>"
			html += "<td>" + str(p[2]) + "</td>"
			html += "<td>@" + str(p[3]) + "</td>"
			html += "<td>" + str(p[4]) + "</td>"
			if (not isEmpty(conn, "gironeA")):
				html += "<td align=\"center\">" + str(p[5]) + "</td>"
			html += "</tr>"
		options={
			'quiet': '',
			'width': '400',
		}
		imgkit.from_string(html, 'out.jpg', options=options)
		context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
		conn.close()
	else:
		pass

handler = CommandHandler('partecipanti', partecipanti)

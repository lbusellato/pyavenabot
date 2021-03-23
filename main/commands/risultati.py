import operator
import sqlite3
import imgkit
from telegram import Update
from telegram.ext import CommandHandler
from auth import auth

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

def getLichessID(tid):
	conn = sqlite3.connect(r".db/avenabot.db")
	player_list = execute(conn, "SELECT * FROM partecipanti")
	for p in player_list:
		if(p[1] == tid):
			conn.close()
			return p[2]
	conn.close()
	return 'null'	

def fetchResults(conn, group):
	html = "<div><table border=\"1\" cellspacing=\"0\" cellpadding=\"4\" align=\"center\"><tr><b>Risultati girone "
	html += group
	table = "girone" + group
	html += "<tr><td></td>"
	player_list = execute(conn, "SELECT * FROM " + table)
	for p in player_list:
		html += "<td align=\"center\">" + str(p[1]) + "</td>"
	html += "</tr>"
	k = 0
	for p in player_list:
		if(k % 2 == 0):
			html += "<tr bgcolor=\"#e9ede4\">"
		else:
			html += "<tr bgcolor=\"#d7edb4\">"
		k += 1
		html += "<td>(" + str(p[1]) + ") " + getLichessID(p[1]) + "</td>"
		for r in p[2]:
			if(r != ","):
				html += "<td width=\"20px\" align=\"center\">"
				if(r == "d"):
					html += "&#189"
				elif(r != "n"):
					html += r
				html += "</td>"
		html += "</tr>"
	html += "</table></div>"
	return html

def risultati(update, context):
	if(auth.auth(update, context)):
		conn = sqlite3.connect(r".db/avenabot.db")
		if(isEmpty(conn, 'gironeF')):
			if(not isEmpty(conn, 'gironeA')):
				html = fetchResults(conn, 'A') + fetchResults(conn, 'B')
				options={
					'quiet': '',
					'width': '600',
				}
				imgkit.from_string(html, 'out.jpg', options=options)
				context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
				conn.close()
		else:
			html = fetchResults(conn, 'F')
			options={
				'quiet': '',
				'width': '400',
			}
			imgkit.from_string(html, 'out.jpg', options=options)
			context.bot.send_photo(update.effective_chat.id, open('./out.jpg', 'rb'))
			conn.close()
			pass
	else:
		pass	

handler = CommandHandler('risultati', risultati)

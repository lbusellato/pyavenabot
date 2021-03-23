from telegram import Update
from telegram.ext import CommandHandler
import imgkit
from auth import auth
from sql import sql

def partecipanti(update, context):
	conn = sql.sql()
	if(auth.auth(update, context)):
		conn.open(r".db/avenabot.db")
		html = '<div><table border="1" cellspacing="0" cellpadding="4" align="center"><tr><th>TID</th><th>ID Lichess</th><th>ID Telegram</th><th>ELO</th>'
		if (not conn.is_empty("gironeA")):
		    html += "<th>Girone</th></tr>"
		player_list = conn.execute("SELECT * FROM partecipanti;")
		#Pull each player's data from the db and nicely format it
		for p in player_list:
			html += "<tr align>"
			html += "<td align=\"center\">" + str(p[1]) + "</td>"
			html += "<td>" + str(p[2]) + "</td>"
			html += "<td>@" + str(p[3]) + "</td>"
			html += "<td>" + str(p[4]) + "</td>"
			if (not conn.is_empty("gironeA")):
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

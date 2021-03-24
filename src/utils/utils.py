from sql import sql
import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError
import logging


def get_player_games(tid):
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	if conn.exists("partecipanti", "tid", str(tid)):
		p_group = conn.execute("SELECT gid FROM partecipanti WHERE tid=" + str(tid) + ";")[0][0]
		games = conn.execute("SELECT res FROM girone" + p_group + " WHERE tid=" + str(tid) + ";")[0][0]
		return games
	else:
		return None


def get_lichess_id(tid):
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	p = conn.execute("SELECT lid FROM partecipanti WHERE tid=" + str(tid) + ";")[0][0]
	conn.close()
	return p


def get_tg_id(tid):
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	p = conn.execute("SELECT tgid FROM partecipanti WHERE tid=" + str(tid) + ";")[0][0]
	conn.close()
	return p


def get_elo(lid):
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	if conn.exists("elo", "lid", lid):
		elo = conn.execute("SELECT ELO FROM elo WHERE lid='" + lid + "';")[0][0]
		conn.close()
		return elo
	else:
		conn.execute("INSERT INTO elo (lid, ELO) VALUES ('" + lid + "',1500);")
		conn.close()
		return 1500


def get_elo_delta(p1_elo, p2_elo, outcome):
	expectation_to_win = 1 / (1 + pow(10, (p2_elo - p1_elo) / 400))
	elo_k = 32
	delta = int(elo_k * (outcome - expectation_to_win))
	return delta


def pull_game(p1, p2):
	url = "https://lichess.org/@/" + p1 + "/all"

	try:
		response = urllib.request.urlopen(url)
	except HTTPError as e:
		logging.error("HTTPError in pull_game(p1, p2): Player not found")
		return [-1, '']
	web_content = response.read().decode()
	i = web_content.find("<article")
	j = web_content.find("article>")
	if i == -1 or j == -1:
		return [-1, '']
	else:
		game = web_content[i:j]
		opponent_check = game.find(p2)
		for k in range(5):
			if opponent_check == -1:
				i = web_content.find("<article", i + 1)
				j = web_content.find("article>", j + 1)
				game = web_content[i:j]
				opponent_check = game.find(p2)
			else:
				break
		if opponent_check == -1:
			return [-1, '']
		else:
			print(game)
			l = game.find("href=\"") + 6
			m = game.find("></a>") - 1
			link = game[l:m]
			result = ''
			if game.find("<span class=\"loss\">") != -1:
				result = '0'
			elif game.find("<span class=\"win\">") != -1:
				result = '1'
			else:
				result = 'd'
			return [result, link]


def get_max_tid():
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	player_list = conn.execute("SELECT * FROM partecipanti;")
	conn.close()
	return player_list[len(player_list) - 1][1]


def get_max_gid(group):
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	player_list = conn.execute("SELECT * FROM girone" + group + ";")
	conn.close()
	return player_list[len(player_list) - 1][1]

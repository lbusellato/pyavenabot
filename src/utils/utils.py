from sql import sql


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


def get_elo_delta(p1_elo, p2_elo, outcome):
	expectation_to_win = 1 / (1 + pow(10, (p2_elo - p1_elo) / 400))
	elo_k = 32
	delta = int(elo_k * (outcome - expectation_to_win))
	return delta

from sql import sql

def getLichessID(tid):
	conn = sql.sql()
	conn.open(r".db/avenabot.db")
	player_list = conn.execute("SELECT * FROM partecipanti;")
	for p in player_list:
		if(p[1] == tid):
			conn.close()
			return p[2]
	conn.close()
	return 'null'	

def get_elo_delta(p1_elo, p2_elo, outcome):
	expectation_to_win = 1 / (1 + pow(10, (p2_elo - p1_elo) / 400))
	elo_K = 32
	delta = int(elo_K * (outcome - expectation_to_win))
	return delta

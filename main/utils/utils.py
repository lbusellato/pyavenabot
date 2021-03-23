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

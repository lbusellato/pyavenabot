import logging
import sqlite3
from sqlite3 import Error


class sql:
	__conn = None
	__open = False

	def open(self, path):
		try:
			self.__conn = sqlite3.connect(path)
			self.__open = True
		except Error as e:
			logging.error("Errore SQL")

	def execute(self, query):
		if self.__open:
			if sqlite3.complete_statement(query):
				try:
					cur = self.__conn.cursor()
					query = query.strip()
					cur.execute(query)
					query_result = cur.fetchall()
					self.__conn.commit()
					return query_result
				except sqlite3.Error as e:
					logging.error("SQL error")
		else:
			logging.warning("DB connection not initialized")
			return None

	def count(self, table):
		if self.__open:
			query = "SELECT count(*) FROM " + table + ";"
			query_result = self.execute(query)
			return query_result[0][0]
		else:
			logging.warning("DB connection not initialized")

	def is_empty(self, table):
		if self.__open:
			return self.count(table) == 0
		else:
			logging.warning("DB connection not initialized")
			return True

	def exists(self, table, key, key_val):
		if self.__open:
			query = "SELECT * FROM " + table + " WHERE " + key + "='" + key_val + "';"
			query_result = self.execute(query)
			return len(query_result)
		else:
			logging.warning("DB connection not initialized")
			return False

	def close(self):
		self.__conn.close()
		self.__open = False

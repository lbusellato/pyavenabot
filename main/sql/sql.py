import logging
import sqlite3
from sqlite3 import Error

class sql:
	__conn = None
	__open = False

	def open(self, path):
		self.__conn = sqlite3.connect(path)
		self.__open = True

	def execute(self, query):
		if(self.__open):
			if sqlite3.complete_statement(query):
				try:
					cur = self.__conn.cursor()
					query = query.strip()
					cur.execute(query)
					return cur.fetchall()
				except sqlite3.Error as e:
					logging.error("SQL error")
		else:
			logging.warning("DB connection not initialized")

	def count(self, table):
		if(self.__open):
			query = "SELECT count(*) FROM " + table + ";"
			query_result = self.execute(query)
			return query_result[0][0]
		else:
			logging.warning("DB connection not initialized")

	def is_empty(self, table):
		if(self.__open):
			return (self.count(table) == 0)
		else:
			logging.warning("DB connection not initialized")
			return 1

	def close(self):
		self.__conn.close()
		self.__open = False


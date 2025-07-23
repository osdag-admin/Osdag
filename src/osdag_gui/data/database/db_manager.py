"""
Database manager for Osdag GUI.
Handles SQLite connection and data fetching utilities.
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parents[3]/ "osdag_core" / "data" / "databases" / "Intg_osdag.sqlite"

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row

    def execute_query(self, query):
        """
        A general-purpose method to execute a given SQL query.
        """
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def fetch_bolt_sizes(self):
        cur = self.conn.cursor()
        cur.execute("SELECT Bolt_diameter FROM Bolt")
        return [str(row["Bolt_diameter"]) for row in cur.fetchall()]

    def fetch_materials(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM Material")
        return [row["name"] for row in cur.fetchall()]
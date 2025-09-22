from osdag_core.Common import *
from pathlib import Path

SQLITE_FILE = files('osdag_gui.data.database')/ 'user_data.sqlite'

PROJECT_TABLE = 'recent_projects'
MODULE_TABLE = 'recent_modules'

ID = 'id'
PROJECT_NAME = 'project_name'
PROJECT_PATH = 'project_path'
CREATION_DATE = 'creation_date'
LAST_EDITED = 'last_edited'
MODULE_KEY = 'module_key'
RELATED_MODULE = 'module'
RELATED_SUBMODULE = 'submodule'
LAST_OPENED = 'opened_at'

MODULE_MAP = {
    #---------Connections-start---------------------------------------------------------
    KEY_DISP_FINPLATE: ['Fin Plate', 'Shear Connection'],
    KEY_DISP_ENDPLATE: ['End Plate', 'Shear Connection'],
    KEY_DISP_CLEATANGLE: ['Cleat Angle', 'Shear Connection'],
    KEY_DISP_SEATED_ANGLE: ['Seated Angle', 'Shear Connection'],

    KEY_DISP_BEAMCOVERPLATE: ['Beam to Beam Cover Plate Bolted', 'Moment Connection'],
    KEY_DISP_BEAMCOVERPLATEWELD: ['Beam to Beam Cover Plate Welded', 'Moment Connection'],
    KEY_DISP_BB_EP_SPLICE: ['Beam-to-Beam End Plate', 'Moment Connection'],

    KEY_DISP_COLUMNCOVERPLATE: ['Column to Column Cover Plate Bolted', 'Moment Connection'],
    KEY_DISP_COLUMNCOVERPLATEWELD: ['Column to Column Cover Plate Welded', 'Moment Connection'],
    KEY_DISP_COLUMNENDPLATE: ['Column-to-Column End Plate', 'Moment Connection'],

    KEY_DISP_BCENDPLATE: ['Beam-to-Column End Plate', 'Moment Connection'],

    KEY_DISP_LAPJOINTBOLTED: ['Lap Joint Bolted', 'Simple Connection'],
    KEY_DISP_LAPJOINTWELDED: ['Lap Joint Welded', 'Simple Connection'],
    KEY_DISP_BUTTJOINTBOLTED: ['Butt Joint Bolted', 'Simple Connection'],
    KEY_DISP_BUTTJOINTWELDED: ['Butt Joint Welded', 'Simple Connection'],

    KEY_DISP_BASE_PLATE: ['Base Plate', 'Connection'],
    #---------Connections-end-----------------------------------------------------------

    #---------Tension-Member-start------------------------------------------------------
    KEY_DISP_TENSION_BOLTED: ['Bolted to End Gusset', 'Tension Member'],
    KEY_DISP_TENSION_WELDED: ['Welded to End Gusset', 'Tension Member'],
    #---------Tension-Member-end------------------------------------------------------

    #---------Compression-Member-start------------------------------------------------------
    KEY_DISP_COMPRESSION_Strut: ['Struts in Trusses', 'Compression Member'],
    KEY_DISP_COMPRESSION_COLUMN: ['Axially Loaded Columns', 'Compression Member'],
    #---------Compression-Member-end------------------------------------------------------

    #---------Flexural-Member-start------------------------------------------------------
    KEY_DISP_FLEXURE: ['Simply Supported Beam', 'Flexural Members'],
    KEY_DISP_FLEXURE2: ['Cantilever Beam', 'Flexural Members'],
    KEY_DISP_FLEXURE4: ['Purlins', 'Flexural Members'],
    KEY_DISP_PLATE_GIRDER_WELDED: ['Plate Girder', 'Flexural Members']
    #---------Flexural-Member-end------------------------------------------------------

}

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict

def create_user_database():
    """
    Ensure SQLite database and required tables exist.
    Creates user_data.sqlite inside the osdag_gui.data.database package if missing.
    """
    sqlitepath = Path(SQLITE_FILE)
    sqlitepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists

    conn = sqlite3.connect(sqlitepath)
    cursor = conn.cursor()

    # Always ensure tables exist
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS recent_projects (
        id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        project_path TEXT NOT NULL UNIQUE,
        module_key TEXT NOT NULL,
        creation_date DATETIME NOT NULL,
        last_edited DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS recent_modules (
        id INTEGER PRIMARY KEY,
        module_key TEXT NOT NULL UNIQUE,
        opened_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print(f"[INFO] Database initialized at: {sqlitepath}")

def format_datetime(dt_str: str) -> str:
    """
    Convert a datetime string from 'YYYY-MM-DD HH:MM:SS' to a readable format like '16 Sep 2025, 14:32'.
    Returns the original string if parsing fails or input is None/empty.
    """
    if not dt_str:
        return dt_str

    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d %b %Y, %H:%M")
    except ValueError:
        return dt_str  # Return if parsing fails

def fetch_all_recent_projects() -> List[Dict]:
    """
    Retrieve all records from recent_projects table, sorted by last opened date descending.
    """
    conn = sqlite3.connect(SQLITE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT {ID}, {PROJECT_NAME}, {PROJECT_PATH}, {MODULE_KEY},
               {CREATION_DATE}, {LAST_EDITED}
        FROM {PROJECT_TABLE}
        ORDER BY {LAST_EDITED} DESC;
    """)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        r = {
            ID: row[0],
            PROJECT_NAME: row[1],
            PROJECT_PATH: row[2],
            RELATED_SUBMODULE: MODULE_MAP.get(row[3])[0],
            CREATION_DATE: format_datetime(row[4]),
            LAST_EDITED: format_datetime(row[5]),
        }
        
        result.append(r)
    return result

def fetch_all_recent_modules() -> list[dict]:
    """
    Retrieve all records from recent_modules table, sorted by last opened date descending.
    """
    records = []
    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT {ID}, {MODULE_KEY}, {LAST_OPENED}
            FROM {MODULE_TABLE}
            ORDER BY {LAST_OPENED} DESC;
        """)
        rows = cursor.fetchall()
        for row in rows:
            dat = MODULE_MAP[row[1]]
            r = {
                ID: row[0],
                RELATED_MODULE: dat[1],
                RELATED_SUBMODULE: dat[0],
                LAST_OPENED: format_datetime(row[2])
            }
            records.append(r)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
    return records

def insert_recent_project(data: dict) -> int | None:
    """
    Insert a new record into recent_projects table.
    Returns:
        ID of the inserted record, or None if insertion failed.
    """
    # Fill missing dates with current timestamp
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    creation_date = data.get("creation_date", now_str)
    last_edited = data.get("last_edited", now_str)

    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        # If there is some conflict in Path(UNIQUE) than last_edited dated is updated.
        cursor.execute(f"""
            INSERT INTO {PROJECT_TABLE} 
            ({PROJECT_NAME}, {PROJECT_PATH}, {MODULE_KEY},{CREATION_DATE}, {LAST_EDITED})
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT({PROJECT_PATH})
            DO UPDATE SET 
                {MODULE_KEY}=excluded.{MODULE_KEY},
                {LAST_EDITED}=excluded.{LAST_EDITED};
        """, (data[PROJECT_NAME], data[PROJECT_PATH], data[MODULE_KEY], creation_date, last_edited))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def insert_recent_module(module_key: str) -> int | None:
    """
    Insert a new record into recent_modules table.
    If the module already exists, update its opened_at timestamp.

    Args:
        module_key (str): Key of the module from MODULE_MAP.
    
    Returns:
        ID of the inserted record, or None if insertion failed.
    """
    opened_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO {MODULE_TABLE} 
            ({MODULE_KEY}, {LAST_OPENED})
            VALUES (?, ?)
            ON CONFLICT({MODULE_KEY})
            DO UPDATE SET 
                {LAST_OPENED}=excluded.{LAST_OPENED};
        """, (module_key, opened_at))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def refactor_database():
    """
    Cleans up the database by:
    1. Removing projects whose file path no longer exists.
    2. Ensuring at most 10 most recent projects remain (drop oldest).
    3. Removing modules older than 60 days.
    4. Ensuring at most 10 most recent modules remain (drop oldest).
    """
    conn = sqlite3.connect(SQLITE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Remove invalid project paths
    cursor.execute(f"SELECT {ID}, {PROJECT_PATH} FROM {PROJECT_TABLE}")
    rows = cursor.fetchall()
    deleted_count = 0
    for row in rows:
        if not Path(row[PROJECT_PATH]).exists():
            cursor.execute(f"DELETE FROM {PROJECT_TABLE} WHERE {ID}=?", (row[ID],))
            deleted_count += 1
    if deleted_count > 0:
        print(f"[INFO] Deleted {deleted_count} project(s) with missing paths.")

    # Keep only 10 most recent projects
    cursor.execute(f"""
        SELECT {ID} FROM {PROJECT_TABLE}
        ORDER BY {LAST_EDITED} DESC
        LIMIT -1 OFFSET 10;
    """)
    rows_to_delete = cursor.fetchall()
    if rows_to_delete:
        ids_to_delete = [str(row[ID]) for row in rows_to_delete]
        cursor.execute(f"DELETE FROM {PROJECT_TABLE} WHERE {ID} IN ({','.join(ids_to_delete)});")
        print(f"[INFO] Deleted {len(ids_to_delete)} oldest project(s) to maintain max 10 records.")

    # Remove modules older than 60 days
    cutoff_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""
        DELETE FROM {MODULE_TABLE}
        WHERE {LAST_OPENED} < ?;
    """, (cutoff_date,))
    old_modules_deleted = cursor.rowcount
    if old_modules_deleted > 0:
        print(f"[INFO] Deleted {old_modules_deleted} module(s) older than 60 days.")

    # Keep only 10 most recent modules
    cursor.execute(f"""
        SELECT {ID} FROM {MODULE_TABLE}
        ORDER BY {LAST_OPENED} DESC
        LIMIT -1 OFFSET 10;
    """)
    rows_to_delete = cursor.fetchall()
    if rows_to_delete:
        ids_to_delete = [str(row[ID]) for row in rows_to_delete]
        cursor.execute(f"DELETE FROM {MODULE_TABLE} WHERE {ID} IN ({','.join(ids_to_delete)});")
        print(f"[INFO] Deleted {len(ids_to_delete)} oldest module(s) to maintain max 10 records.")

    conn.commit()
    conn.close()
    print("[INFO] Database cleanup complete.") 

def main():
    print("=== Testing User Database Functions ===")

    print("\n[INFO] Creating/Updating database if needed...")
    create_user_database()

    # === Insert Dummy Projects for ALL MODULES ===
    print("\n[INFO] Inserting dummy projects for all modules...")
    for i, (module_key, module_info) in enumerate(MODULE_MAP.items(), start=1):
        sample_project = {
            PROJECT_NAME: f"Dummy Project {i} - {module_info[0]}",
            PROJECT_PATH: f"C:/Users/Me/Documents/dummy_project_{i}.osdag",
            MODULE_KEY: module_key,
        }
        inserted_id = insert_recent_project(sample_project)
        if inserted_id:
            print(f"[SUCCESS] Inserted project ID: {inserted_id} ({module_info[0]})")
        else:
            print(f"[ERROR] Failed to insert project for {module_info[0]}")

    # === Insert Dummy Modules for ALL MODULES ===
    print("\n[INFO] Inserting dummy modules for all modules...")
    for module_key, module_info in MODULE_MAP.items():
        inserted_module_id = insert_recent_module(module_key)
        if inserted_module_id:
            print(f"[SUCCESS] Inserted module: {module_info[0]} ({module_info[1]})")
        else:
            print(f"[ERROR] Failed to insert module for {module_info[0]}")

    # === Fetch & Display Results ===
    print("\n=== Recent Projects ===")
    projects = fetch_all_recent_projects()
    for p in projects:
        print(f"- {p[PROJECT_NAME]} ({p[PROJECT_PATH]})")
        print(f"  Submodule: {p[RELATED_SUBMODULE]}")
        print(f"  Created: {p[CREATION_DATE]}, Last Edited: {p[LAST_EDITED]}")
        print("")

    print("=== Recent Modules ===")
    modules = fetch_all_recent_modules()
    for m in modules:
        print(f"- {m[RELATED_MODULE]} > {m[RELATED_SUBMODULE]} (Opened: {m[LAST_OPENED]})")

if __name__=="__main__":
    create_user_database()
    main()
    # print(fetch_all_recent_modules())
    # print(fetch_all_recent_projects())
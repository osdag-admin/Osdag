from osdag_core.Common import (KEY_DISP_FINPLATE, KEY_DISP_ENDPLATE, KEY_DISP_CLEATANGLE, KEY_DISP_SEATED_ANGLE, KEY_DISP_BEAMCOVERPLATE,
                               KEY_DISP_BEAMCOVERPLATEWELD, KEY_DISP_BB_EP_SPLICE, KEY_DISP_COLUMNCOVERPLATE, KEY_DISP_COLUMNCOVERPLATEWELD,
                               KEY_DISP_COLUMNENDPLATE, KEY_DISP_BCENDPLATE, KEY_DISP_LAPJOINTBOLTED, KEY_DISP_LAPJOINTWELDED, KEY_DISP_BUTTJOINTBOLTED,
                               KEY_DISP_BUTTJOINTWELDED, KEY_DISP_BASE_PLATE, KEY_DISP_TENSION_BOLTED, KEY_DISP_TENSION_WELDED, KEY_DISP_COMPRESSION_Strut,
                               KEY_DISP_COMPRESSION_COLUMN, KEY_DISP_FLEXURE, KEY_DISP_FLEXURE2, KEY_DISP_FLEXURE4, KEY_DISP_PLATE_GIRDER_WELDED)
from pathlib import Path
from importlib.resources import files

SQLITE_FILE = files('osdag_gui.data.database')/ 'user_data.sqlite'

PROJECT_TABLE = 'recent_projects'
MODULE_TABLE = 'recent_modules'

KEY_SEARCH_MODULE = 'modules'
KEY_SEARCH_PROJ = 'projects'

ID = 'id'
PROJECT_NAME = 'project_name'
PROJECT_PATH = 'project_path'
CREATION_DATE = 'creation_date'
LAST_EDITED = 'last_edited'
MODULE_KEY = 'module_key'
RELATED_MODULE = 'module'
RELATED_SUBMODULE = 'submodule'
LAST_OPENED = 'opened_at'
REPORT_FILE_PATH = 'files_path'

#------------------------------------Search-logic-start------------------------------------------------------------
SEARCH_MODULE_MAP = {
    'Fin Plate Shear Connection': KEY_DISP_FINPLATE,
    'End Plate Shear Connection': KEY_DISP_ENDPLATE,
    'Cleat Angle Shear Connection': KEY_DISP_CLEATANGLE,
    'Seated Angle Shear Connection': KEY_DISP_SEATED_ANGLE,
    'Beam to Beam Cover Plate Bolted Moment Connection': KEY_DISP_BEAMCOVERPLATE,
    'Beam to Beam Cover Plate Welded Moment Connection': KEY_DISP_BEAMCOVERPLATEWELD,
    'Beam to Beam End Plate Moment Connection': KEY_DISP_BB_EP_SPLICE,
    'Column to Column Cover Plate Bolted Moment Connection': KEY_DISP_COLUMNCOVERPLATE,
    'Column to Column Cover Plate Welded Moment Connection': KEY_DISP_COLUMNCOVERPLATEWELD,
    'Column to Column End Plate Moment Connection': KEY_DISP_COLUMNENDPLATE,
    'Beam to Column End Plate Moment Connection': KEY_DISP_BCENDPLATE,
    'Lap Joint Bolted Simple Connection': KEY_DISP_LAPJOINTBOLTED,
    'Lap Joint Welded Simple Connection': KEY_DISP_LAPJOINTWELDED,
    'Butt Joint Bolted Simple Connection': KEY_DISP_BUTTJOINTBOLTED,
    'Butt Joint Welded Simple Connection': KEY_DISP_BUTTJOINTWELDED,
    'Base Plate Connection': KEY_DISP_BASE_PLATE,
    'Bolted to End Gusset Tension Member': KEY_DISP_TENSION_BOLTED,
    'Welded to End Gusset Tension Member': KEY_DISP_TENSION_WELDED,
    'Struts in Trusses Compression Member': KEY_DISP_COMPRESSION_Strut,
    'Axially Loaded Columns Compression Member': KEY_DISP_COMPRESSION_COLUMN,
    'Simply Supported Beam Flexural Member': KEY_DISP_FLEXURE,
    'Cantilever Beam Flexural Member': KEY_DISP_FLEXURE2,
    'Purlins Flexural Member': KEY_DISP_FLEXURE4,
    'Plate Girder Flexural Member': KEY_DISP_PLATE_GIRDER_WELDED
}

def _search_modules(keywords: list, module_map:dict = SEARCH_MODULE_MAP) -> list[tuple]:
    """
    Search modules by keyword(s).
    
    Args:
        query: str or list of str
            - str: "beam plate" (space-separated keywords)
        module_map: dict with module names as keys
    
    Returns:
        list of (module_key, score) tuples, sorted by relevance
    """

    results = []
    
    for module_name, module_key in module_map.items():
        module_lower = module_name.lower()
        
        # Count matching keywords
        score = 0
        matched_count = 0
        
        for keyword in keywords:
            if keyword in module_lower:
                matched_count += 1
                # Exact word match gets higher score
                if f" {keyword} " in f" {module_lower} ":
                    score += 3
                else:
                    score += 2
        
        # Only include if at least one keyword matches
        if matched_count > 0:
            # Bonus for matching all keywords
            if matched_count == len(keywords):
                score += 5
            
            results.append((module_key, score))
    
    # Sort by score descending
    results.sort(key=lambda x: -x[1])
    return results

def _search_projects(keywords: list, module_keys: list[tuple]) -> list[dict]:
    """
    Search recent_projects by project_name keyword(s) and module_key.
    
    Args:
        keywords: list - lowercase keywords from query
        module_keys: List[tuple] - list of (module_key, score) tuples from module search
    
    Returns:
        List of project dicts sorted by relevance score, then by last_edited
    """  
    # Extract module keys for filtering
    matched_module_keys = {mk[0] for mk in module_keys} if module_keys else set()

    conn = sqlite3.connect(SQLITE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(f"""
        SELECT {ID}, {PROJECT_NAME}, {PROJECT_PATH}, {MODULE_KEY},
               {CREATION_DATE}, {LAST_EDITED}
        FROM {PROJECT_TABLE}
    """)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    
    for row in rows:
        project_name_lower = row[1].lower()
        project_module_key = row[3]  # Get project's module_key
        
        # Calculate relevance score
        score = 0
        matched_count = 0
        matched_by_module = False  # Track if matched by module
        
        # Check if project's module_key matches any searched modules
        if project_module_key in matched_module_keys:
            matched_by_module = True
            # Get the module's search score
            module_score = next((ms[1] for ms in module_keys if ms[0] == project_module_key), 0)
            score += module_score  # Add module relevance to project score
        
        # Search in project_name
        for keyword in keywords:
            if keyword in project_name_lower:
                matched_count += 1
                # Exact word match gets higher score
                if f" {keyword} " in f" {project_name_lower} ":
                    score += 3
                # Match at start of name
                elif project_name_lower.startswith(keyword):
                    score += 4
                else:
                    score += 2
        
        if matched_by_module or matched_count > 0:
            # Bonus for matching all keywords in project name
            if matched_count == len(keywords):
                score += 5
            
            project_dict = {
                ID: row[0],
                PROJECT_NAME: row[1],
                PROJECT_PATH: row[2],
                RELATED_SUBMODULE: MODULE_MAP.get(row[3])[0],
                CREATION_DATE: _format_datetime(row[4]),
                LAST_EDITED: _format_datetime(row[5]),
                'score': score
            }
            
            results.append(project_dict)
    
    # Sort by score descending, then by last_edited descending
    results.sort(key=lambda x: (-x['score'], x[LAST_EDITED]), reverse=False)
    
    return results

def _get_module_data(keys: list[tuple]) -> list[dict]:
    records = []
    for key, _ in keys:
        dat = MODULE_MAP[key]
        r = {
            MODULE_KEY: key,
            RELATED_MODULE: dat[1],
            RELATED_SUBMODULE: dat[0],
        }
        records.append(r)
    
    return records

def search_projects_and_modules(query: str) -> dict[str, list]:
    """
    Search both projects and modules with a single query.
    
    Args:
        query: str - space-separated keywords
    
    Returns:
        dict with 'projects' and 'modules' keys containing search results
    """
    keywords = query.lower().split()
    if not keywords:
        return {}

    modules = _search_modules(keywords)

    return {
        KEY_SEARCH_PROJ: _search_projects(keywords, modules),
        KEY_SEARCH_MODULE: _get_module_data(modules)
    }
#------------------------------------Search-logic-end------------------------------------------------------------

MODULE_MAP = {
    #----------------------------Connections-start-------------------------------------
    #--------------------Submodule---------Module---------Open-module-function---------
    KEY_DISP_FINPLATE: ['Fin Plate', 'Shear Connection', 'open_fin_plate_page'],
    KEY_DISP_ENDPLATE: ['End Plate', 'Shear Connection', 'None'],
    KEY_DISP_CLEATANGLE: ['Cleat Angle', 'Shear Connection', 'None'],
    KEY_DISP_SEATED_ANGLE: ['Seated Angle', 'Shear Connection', 'None'],

    KEY_DISP_BEAMCOVERPLATE: ['Beam to Beam Cover Plate Bolted', 'Moment Connection', 'None'],
    KEY_DISP_BEAMCOVERPLATEWELD: ['Beam to Beam Cover Plate Welded', 'Moment Connection', 'None'],
    KEY_DISP_BB_EP_SPLICE: ['Beam-to-Beam End Plate', 'Moment Connection', 'None'],

    KEY_DISP_COLUMNCOVERPLATE: ['Column to Column Cover Plate Bolted', 'Moment Connection', 'None'],
    KEY_DISP_COLUMNCOVERPLATEWELD: ['Column to Column Cover Plate Welded', 'Moment Connection', 'None'],
    KEY_DISP_COLUMNENDPLATE: ['Column-to-Column End Plate', 'Moment Connection', 'None'],

    KEY_DISP_BCENDPLATE: ['Beam-to-Column End Plate', 'Moment Connection', 'None'],

    KEY_DISP_LAPJOINTBOLTED: ['Lap Joint Bolted', 'Simple Connection', 'None'],
    KEY_DISP_LAPJOINTWELDED: ['Lap Joint Welded', 'Simple Connection', 'None'],
    KEY_DISP_BUTTJOINTBOLTED: ['Butt Joint Bolted', 'Simple Connection', 'None'],
    KEY_DISP_BUTTJOINTWELDED: ['Butt Joint Welded', 'Simple Connection', 'None'],

    KEY_DISP_BASE_PLATE: ['Base Plate', 'Connection', 'None'],
    #---------Connections-end-----------------------------------------------------------

    #---------Tension-Member-start------------------------------------------------------
    KEY_DISP_TENSION_BOLTED: ['Bolted to End Gusset', 'Tension Member', 'None'],
    KEY_DISP_TENSION_WELDED: ['Welded to End Gusset', 'Tension Member', 'None'],
    #---------Tension-Member-end------------------------------------------------------

    #---------Compression-Member-start------------------------------------------------------
    KEY_DISP_COMPRESSION_Strut: ['Struts in Trusses', 'Compression Member', 'None'],
    KEY_DISP_COMPRESSION_COLUMN: ['Axially Loaded Columns', 'Compression Member', 'None'],
    #---------Compression-Member-end------------------------------------------------------

    #---------Flexural-Member-start------------------------------------------------------
    KEY_DISP_FLEXURE: ['Simply Supported Beam', 'Flexural Members', 'None'],
    KEY_DISP_FLEXURE2: ['Cantilever Beam', 'Flexural Members', 'None'],
    KEY_DISP_FLEXURE4: ['Purlins', 'Flexural Members', 'None'],
    KEY_DISP_PLATE_GIRDER_WELDED: ['Plate Girder', 'Flexural Members', 'None']
    #---------Flexural-Member-end------------------------------------------------------

}

# To retrieve the name of a module function that can open the required module
def get_module_function(key: str):
    return MODULE_MAP[key][2]

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
        files_path TEXT NOT NULL,
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

def _format_datetime(dt_str: str) -> str:
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
            CREATION_DATE: _format_datetime(row[4]),
            LAST_EDITED: _format_datetime(row[5]),
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
                MODULE_KEY: row[1],
                RELATED_MODULE: dat[1],
                RELATED_SUBMODULE: dat[0],
                LAST_OPENED: _format_datetime(row[2])
            }
            records.append(r)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()
    return records

def delete_project_record(project_id: int) -> bool:
    """
    Delete a project record from the recent_projects table using its ID.

    Args:
        project_id (int): The ID of the project to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {PROJECT_TABLE} WHERE {ID} = ?;", (project_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def update_project_path(project_id: int, new_path: str, new_name: str) -> int | None:
    """
    Update the project_path and project_name for a project in the recent_projects table using its ID.
    If the new_path already exists in another record (with a different ID), delete those records,
    then update the file name and path in the given id.

    Args:
        project_id (int): The ID of the project to update.
        new_path (str): The new project path.
        new_name (str): The new project name.

    Returns:
        int | None: The ID of the updated record (project_id) if update was successful,
                    or None if an error occurred.
    """
    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        # Find and delete any records with the same path but a different id
        cursor.execute(f"SELECT {ID} FROM {PROJECT_TABLE} WHERE {PROJECT_PATH} = ? AND {ID} != ?;", (new_path, project_id))
        rows = cursor.fetchall()
        for row in rows:
            conflict_id = row[0]
            cursor.execute(f"DELETE FROM {PROJECT_TABLE} WHERE {ID} = ?;", (conflict_id,))
        # Now update the path and name for the given id
        cursor.execute(
            f"UPDATE {PROJECT_TABLE} SET {PROJECT_PATH} = ?, {PROJECT_NAME} = ? WHERE {ID} = ?;",
            (new_path, new_name, project_id)
        )
        conn.commit()
        return project_id
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_project_by_id(project_id: int) -> dict | None:
    """
    Retrieve project data from the recent_projects table for the given project ID.

    Args:
        project_id (int): The ID of the project to retrieve.

    Returns:
        dict | None: Dictionary containing project data if found, else None.
    """
    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {ID}, {PROJECT_NAME}, {PROJECT_PATH}, {MODULE_KEY}, {CREATION_DATE}, {LAST_EDITED} "
            f"FROM {PROJECT_TABLE} WHERE {ID} = ?;",
            (project_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                ID: row[0],
                PROJECT_NAME: row[1],
                PROJECT_PATH: row[2]
            }
        else:
            return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
            conn.close()

def insert_recent_project(data: dict) -> int | None:
    """
    Insert a new record into the recent_projects table.
    
    data (dict): Dictionary containing project details. Must include keys:
            - PROJECT_NAME: Name of the project
            - PROJECT_PATH: Path to the project (unique identifier)
            - MODULE_KEY: Module identifier
            - FILES_PATH: Path to .tex and .pngs
            Optional keys:
            - creation_date: Creation timestamp (defaults to current time)
            - last_edited: Last edited timestamp (defaults to current time)
    Returns:
        int | None: ID of the inserted or updated record, or None if insertion failed.
    """
    # Fill missing dates with current timestamp
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    creation_date = data.get("creation_date", now_str)
    last_edited = data.get("last_edited", now_str)

    try:
        conn = sqlite3.connect(SQLITE_FILE)
        cursor = conn.cursor()
        # If there is some conflict in Path(UNIQUE) then last_edited date is updated.
        cursor.execute(f"""
            INSERT INTO {PROJECT_TABLE} 
            ({PROJECT_NAME}, {PROJECT_PATH}, {REPORT_FILE_PATH}, {MODULE_KEY}, {CREATION_DATE}, {LAST_EDITED})
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT({PROJECT_PATH})
            DO UPDATE SET 
                {MODULE_KEY}=excluded.{MODULE_KEY},
                {LAST_EDITED}=excluded.{LAST_EDITED};
        """, (
            data[PROJECT_NAME],
            data[PROJECT_PATH],
            data[REPORT_FILE_PATH],
            data[MODULE_KEY],
            creation_date,
            last_edited
        ))
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

    # Remove projects older than 60 days
    cutoff_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(f"""
        DELETE FROM {PROJECT_TABLE}
        WHERE {LAST_EDITED} < ?;
    """, (cutoff_date,))
    old_modules_deleted = cursor.rowcount
    if old_modules_deleted > 0:
        print(f"[INFO] Deleted {old_modules_deleted} project records older than 60 days.")

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
    cursor.execute(f"""
        DELETE FROM {MODULE_TABLE}
        WHERE {LAST_OPENED} < ?;
    """, (cutoff_date,))
    old_modules_deleted = cursor.rowcount
    if old_modules_deleted > 0:
        print(f"[INFO] Deleted {old_modules_deleted} module records older than 60 days.")

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
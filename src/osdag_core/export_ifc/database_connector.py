import sqlite3
from pathlib import Path

def get_db_path():
    """
    Locates the main Intg_osdag.sqlite mechanical structural database.
    """
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / 'data' / 'ResourceFiles' / 'Database' / 'Intg_osdag.sqlite'

def fetch_profile_data(designation, profile_type=""):
    """
    Queries all structural profile tables to find the matching standard dimensions.
    Returns dictionary with Mass (kg/m) and Area (cm^2) if found.
    """
    db_path = get_db_path()
    if not db_path.exists():
        return None
        
    tables = ['Beams', 'Columns', 'Channels', 'Angles', 'EqualAngle', 'UnequalAngle', 'RHS', 'SHS', 'CHS']
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        for table in tables:
            try:
                # Hollow sections (RHS, SHS, CHS) use 'W' and 'A' instead of 'Mass' and 'Area'
                if table in ['RHS', 'SHS', 'CHS']:
                    cursor.execute(f"SELECT W as Mass, A as Area FROM {table} WHERE Designation COLLATE NOCASE = ?", (designation,))
                else:
                    cursor.execute(f"SELECT Mass, Area FROM {table} WHERE Designation COLLATE NOCASE = ?", (designation,))
                    
                row = cursor.fetchone()
                if row:
                    return dict(row)
            except sqlite3.OperationalError:
                # Table might not exist or schema differs
                continue
                
        return None
    except Exception as e:
        print(f"[IFC Exporter] DB Lookup Error: {e}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()

def fetch_bolt_data(grade):
    """
    Queries the properties of standard bolts through their grade parameter.
    """
    db_path = get_db_path()
    if not db_path.exists():
        return None
        
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # The column is called Property_Class
        cursor.execute("SELECT fy, fu FROM Bolt_fy_fu WHERE Property_Class = ?", (str(grade),))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        return None
    finally:
        if 'conn' in locals():
            conn.close()

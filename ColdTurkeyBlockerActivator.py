import json
import sqlite3
import os

DB_PATH = "C:/ProgramData/Cold Turkey/data-app.db"

def activate():
    conn = None  # Initialize conn to None to handle exceptions during connection
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Fetch settings
        result = c.execute("SELECT value FROM settings WHERE key = 'settings'").fetchone()
        if not result:
            print("No settings found in the database.")
            return
        
        s = result[0]
        dat = json.loads(s)
        
        # Check and update proStatus
        additional = dat.setdefault("additional", {})  # Safely get 'additional' key
        if additional.get("proStatus") != "pro":
            print("Your version of Cold Turkey Blocker is not activated.")
            additional["proStatus"] = "pro"
            print("But now it is activated.\nPlease close Cold Turkey Blocker and run it again.")
        else:
            print("Looks like your copy of Cold Turkey Blocker is already activated.")
            print("Deactivating it now.")
            additional["proStatus"] = "free"
        
        # Update the database
        c.execute("UPDATE settings SET value = ? WHERE key = 'settings'", (json.dumps(dat),))
        conn.commit()

    except sqlite3.Error as e:
        print("Failed to activate:", e)
    except json.JSONDecodeError as e:
        print("Failed to parse settings JSON:", e)
    except KeyError as e:
        print("Key error in settings data:", e)
    finally:
        if conn:
            conn.close()

def main():
    if os.path.exists(DB_PATH):
        print("Data file found.\nLet's activate your copy of Cold Turkey Blocker.")
        activate()
    else:
        print("Looks like Cold Turkey Blocker is not installed.\nIf it is installed, please run it at least once.")

if __name__ == '__main__':
    main()
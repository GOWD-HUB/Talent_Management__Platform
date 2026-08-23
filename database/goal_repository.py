from datetime import datetime
from database.connection import get_connection

def create_goal_table():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS school_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT DEFAULT '',
        target_date TEXT DEFAULT '',
        priority TEXT DEFAULT 'Medium',
        status TEXT DEFAULT 'Active',
        milestones TEXT DEFAULT '',
        completed_milestones TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)
    con.commit()
    con.close()

def _join(items):
    return "|||".join([str(x).strip() for x in (items or []) if str(x).strip()])

def _split(value):
    return [x.strip() for x in str(value or "").split("|||") if x.strip()]

def create_goal(user_id, title, category, description, target_date, priority, milestones):
    create_goal_table()
    now = datetime.now().isoformat()
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
    INSERT INTO school_goals
    (user_id,title,category,description,target_date,priority,status,milestones,completed_milestones,created_at,updated_at)
    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (user_id,title.strip(),category,description.strip(),target_date,priority,"Active",_join(milestones),"",now,now))
    con.commit()
    con.close()

def get_goals(user_id):
    create_goal_table()
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM school_goals WHERE user_id=? ORDER BY target_date ASC, id DESC", (user_id,))
    rows = cur.fetchall()
    con.close()
    result = []
    for row in rows:
        try:
            item = dict(row)
        except Exception:
            cols = ["id","user_id","title","category","description","target_date","priority","status","milestones","completed_milestones","created_at","updated_at"]
            item = dict(zip(cols,row))
        item["milestones"] = _split(item.get("milestones"))
        item["completed_milestones"] = _split(item.get("completed_milestones"))
        result.append(item)
    return result

def update_goal_progress(goal_id, completed_milestones):
    create_goal_table()
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT milestones FROM school_goals WHERE id=?", (goal_id,))
    row = cur.fetchone()
    if not row:
        con.close()
        return
    try:
        milestones = _split(row["milestones"])
    except Exception:
        milestones = _split(row[0])
    completed = [x for x in completed_milestones if x in milestones]
    status = "Completed" if milestones and len(completed) == len(milestones) else "Active"
    cur.execute("""
    UPDATE school_goals
    SET completed_milestones=?, status=?, updated_at=?
    WHERE id=?
    """, (_join(completed),status,datetime.now().isoformat(),goal_id))
    con.commit()
    con.close()

def update_goal(goal_id, title, category, description, target_date, priority, milestones):
    create_goal_table()
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT completed_milestones FROM school_goals WHERE id=?", (goal_id,))
    row = cur.fetchone()
    completed = []
    if row:
        try:
            completed = _split(row["completed_milestones"])
        except Exception:
            completed = _split(row[0])
    milestones = [str(x).strip() for x in milestones if str(x).strip()]
    completed = [x for x in completed if x in milestones]
    status = "Completed" if milestones and len(completed) == len(milestones) else "Active"
    cur.execute("""
    UPDATE school_goals SET title=?,category=?,description=?,target_date=?,priority=?,
    status=?,milestones=?,completed_milestones=?,updated_at=? WHERE id=?
    """, (title.strip(),category,description.strip(),target_date,priority,status,_join(milestones),_join(completed),datetime.now().isoformat(),goal_id))
    con.commit()
    con.close()

def delete_goal(goal_id):
    create_goal_table()
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM school_goals WHERE id=?", (goal_id,))
    con.commit()
    con.close()

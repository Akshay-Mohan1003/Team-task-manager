import sqlite3
import json
import os
import uuid
import datetime

db_path = "local.db"

def migrate():
    if not os.path.exists(db_path):
        print("local.db not found. Run the app to create it.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Alter Tasks table
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN task_type VARCHAR(50) DEFAULT 'human_hitl'")
        print("Added task_type to tasks.")
    except sqlite3.OperationalError as e:
        print(f"Skipped task_type: {e}")

    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN compute_estimated_tokens INTEGER DEFAULT 0")
        print("Added compute_estimated_tokens to tasks.")
    except sqlite3.OperationalError as e:
        print(f"Skipped compute_estimated_tokens: {e}")

    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN processing_logs JSON DEFAULT '[]'")
        print("Added processing_logs to tasks.")
    except sqlite3.OperationalError as e:
        print(f"Skipped processing_logs: {e}")

    # Create project_members table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_members (
        id VARCHAR PRIMARY KEY,
        project_id VARCHAR NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        role VARCHAR(50) NOT NULL DEFAULT 'Member'
    )
    """)
    print("Created project_members table.")

    # Create platform_telemetry table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platform_telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id VARCHAR NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        log_level VARCHAR(10) DEFAULT 'INFO',
        subsystem VARCHAR(50) NOT NULL,
        message VARCHAR NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Created platform_telemetry table.")

    # Migrate existing project owners to project_members as Admin
    cursor.execute("SELECT id, owner_id FROM projects WHERE owner_id IS NOT NULL")
    projects = cursor.fetchall()
    for proj_id, owner_id in projects:
        cursor.execute("SELECT id FROM project_members WHERE project_id=? AND user_id=?", (proj_id, owner_id))
        if not cursor.fetchone():
            pm_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO project_members (id, project_id, user_id, role) VALUES (?, ?, ?, ?)", (pm_id, proj_id, owner_id, 'Admin'))
            print(f"Added owner {owner_id} as Admin for project {proj_id}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()

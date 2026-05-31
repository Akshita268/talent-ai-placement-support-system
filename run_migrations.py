import sqlite3
import os

def run_migrations():
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'site.db')
    print(f"Connecting to database at {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Structure of updates: (table_name, column_name, column_type)
    updates = [
        ('student', 'target_role', 'VARCHAR(100)'),
        ('student', 'career_recommendation', 'TEXT'),
        ('student', 'learning_roadmap', 'TEXT'),
        
        ('application', 'embedding_score', 'FLOAT'),
        ('application', 'skill_score', 'FLOAT'),
        ('application', 'project_score', 'FLOAT'),
        
        ('interview_answer', 'communication_score', 'FLOAT'),
        ('interview_answer', 'confidence_score', 'FLOAT'),
        ('interview_answer', 'leadership_score', 'FLOAT'),
        ('interview_answer', 'problem_solving_score', 'FLOAT'),
        ('interview_answer', 'improved_answer', 'TEXT'),
        
        ('technical_interview_answer', 'topic_score', 'FLOAT'),
        ('technical_interview_answer', 'weak_areas', 'TEXT'),
        ('technical_interview_answer', 'strong_areas', 'TEXT'),
        ('technical_interview_answer', 'suggested_better_answer', 'TEXT'),
        
        ('coding_problem', 'company_tags', 'TEXT'),
        ('coding_problem', 'hints', 'TEXT'),
        ('coding_problem', 'complexity_analysis', 'TEXT'),
        ('notification', 'recruiter_id', 'INTEGER'),
        ('application', 'recruiter_notes', 'TEXT')
    ]
    
    for table, col, col_type in updates:
        try:
            # Check if column exists by listing table info
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in cursor.fetchall()]
            
            if col not in columns:
                print(f"Adding column {col} ({col_type}) to table {table}...")
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
                conn.commit()
            else:
                print(f"Column {col} already exists in table {table}.")
        except Exception as e:
            print(f"Error migrating {table}.{col}: {e}")
            
    conn.close()
    print("Database migration completed.")

if __name__ == '__main__':
    run_migrations()

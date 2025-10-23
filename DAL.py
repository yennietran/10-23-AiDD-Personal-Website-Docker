import sqlite3

def get_connection(db_path="projects.db"):
    """Get a database connection with Row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path="projects.db"):
    """Initialize the database and create projects table if it doesn't exist."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image_filename TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def insert_project(title, description, image_filename):
    """Insert a new project into the database."""
    conn = get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO projects (title, description, image_filename) VALUES (?, ?, ?)"
    cur.execute(sql, (title, description, image_filename))
    conn.commit()
    conn.close()

def get_projects():
    """Get all projects ordered by created_at DESC, returned as list of dictionaries."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, image_filename, created_at FROM projects ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    
    # Convert Row objects to dictionaries
    projects_list = []
    for row in rows:
        project_dict = {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "image_filename": row["image_filename"],
            "created_at": row["created_at"]
        }
        projects_list.append(project_dict)
    
    return projects_list

if __name__ == "__main__":
    # Initialize database and seed with sample data if empty
    init_db()
    projects = get_projects()
    if len(projects) == 0:
        print("Seeding database with sample projects...")
        insert_project(
            "FCRE Racing Website",
            "In the summer of 2025, I participated in a required Jumpstart Program designed to equip students with essential skills for the upcoming MSIS fall semester. During this program, I built my first website from the ground up using HTML, CSS, and Bootstrap. The project, titled FCRE (Four Circles Racing Events), is a mock company that provides a Formula 1–style driving experience for group events. The website consists of seven pages — Home, About Us, Events, Specials, Logistics Approval, Participant Survey, and New Event. Through this project (naming a few), I learned how to structure and style content using containers, design a responsive navigation bar, embed links, insert images, and build tables to display information effectively. Overall, this experience taught me the fundamentals of front-end development and how to create a simple, functional, and client-ready website from scratch.",
            "fcre home.png" 
        )
        insert_project(
            "iPhone Recommender Chatbot",
            "During the fall semester of the MSIS program, I took an AI course where we learned how to design and develop chatbots. Using Dialogflow, my team and I created a chatbot named Bob that helps users find the most suitable iPhone based on their preferences. The chatbot asks a series of questions about key criteria such as phone size (small, medium, or large), storage capacity (256 GB, 512 GB, or 1 TB), and the number of cameras (2 or 3). Based on the user's responses, Bob recommends an iPhone model currently available on the market. Each recommendation includes the iPhone version, a breakdown of the requested specifications, and the price. The chatbot also features built-in fallback responses to handle unclear input gracefully and can restart the conversation if the user wants to search for another device. There are a lot of options, so feel free to play around with it!",
            "chatbot1.png"
        )
        print("Database seeded successfully!")
    else:
        print(f"Database already contains {len(projects)} project(s).")

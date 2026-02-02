import mysql.connector
import time

# Wait for MySQL to be ready
time.sleep(5)

conn = mysql.connector.connect(
    host="mysql",          # MySQL container name
    user="root",
    password="rootpassword",
    database="testdb"
)

cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
)
""")
conn.commit()

def add_user():
    name = input("Enter name to add: ")
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()
    print("✅ User added successfully\n")

def read_users():
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    if not rows:
        print("📭 No users found\n")
        return

    print("\n📋 Users in database:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}")
    print()

while True:
    print("Choose an option:")
    print("1. Add user")
    print("2. Read all users")
    print("3. Exit")

    choice = input("Enter choice (1/2/3): ")

    if choice == "1":
        add_user()
    elif choice == "2":
        read_users()
    elif choice == "3":
        print("👋 Exiting...")
        break
    else:
        print("❌ Invalid choice\n")

cursor.close()
conn.close()

import sqlite3

# Database setup
connection=sqlite3.connect("student.db")

# Create cursor
cursor=connection.cursor()

# Create the table
create_table_query="""
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME    VARCHAR(25),
    COURSE   VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS   INT
);
"""

cursor.execute(create_table_query)

# Insert Records
sql_query = """INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS) VALUES (?, ?, ?, ?)"""
values = [
    ('Ajay', 'Data Science', 'A', 90),
    ('Anuj', 'Data Science', 'B', 100),
    ('Ganesh', 'Data Science', 'A', 86),
    ('Prince', 'DEVOPS', 'A', 50),
    ('Nitin', 'DEVOPS', 'A', 35),
    ('Abhinit', 'Machine learning', 'A', 95),
    ('Sujeet', 'NLLP', 'B', 100),
    ('Anmol', 'DEVOPS', 'A', 65),
    ('RaJ', 'DEVOPS', 'B', 76),
    ('Sachin', 'Machine learning', 'A', 85),
    ('Ashu', 'Data Science', 'A', 60),
    ('David', 'DEVOPS', 'B', 40),
    ('Shiva', 'Machine learninng', 'B', 86),
    ('Avdhut', 'DEVOPS', 'A', 100),
    ('Rahul', 'Machine learning', 'A', 100),
    ('Ajay', 'Data Science', 'A', 90),
    ('Neha', 'Machine Learning', 'B', 82),
    ('Rahul', 'AI Ethics', 'A', 88),
    ('Priya', 'Deep Learning', 'C', 75),
    ('Vikram', 'Computer Vision', 'B', 84),
    ('Simran', 'Natural Language Processing', 'A', 91),
    ('Ankit', 'Data Engineering', 'B', 80),
    ('Riya', 'Reinforcement Learning', 'C', 72),
    ('Karan', 'Time Series Analysis', 'A', 89),
    ('Isha', 'Big Data Analytics', 'B', 83),
    ('Arjun', 'Statistics', 'A', 86),
    ('Sneha', 'Data Visualization', 'B', 81),
    ('Rakesh', 'Data Mining', 'C', 78),
    ('Tanya', 'Python for Data Science', 'A', 93),
    ('Dev', 'SQL Optimization', 'B', 79),
    ('mani', 'Bayesian Methods', 'A', 90),
    ('Harsh', 'Model Evaluation', 'B', 85),
    ('Meera', 'Feature Engineering', 'C', 76),
    ('Sahil', 'TensorFlow Basics', 'B', 82),
    ('Aarti', 'MLOps', 'A', 87),

]

cursor.executemany(sql_query, values)
connection.commit()

# Display the records
data=cursor.execute("""Select * from STUDENT""")

for row in data:
    print(row)

if connection:
    connection.close()
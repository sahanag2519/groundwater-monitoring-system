
import sqlite3

connection = sqlite3.connect("groundwater.db")

cursor = connection.cursor()

# Add village column if it does not already exist
try:
    cursor.execute(
        "ALTER TABLE sensor_data ADD COLUMN village TEXT"
    )
except sqlite3.OperationalError:
    pass

# Add well column if it does not already exist
try:
    cursor.execute(
        "ALTER TABLE sensor_data ADD COLUMN well TEXT"
    )
except sqlite3.OperationalError:
    pass

# Give existing readings default values
cursor.execute("""
UPDATE sensor_data
SET village = 'Village A'
WHERE village IS NULL
""")

cursor.execute("""
UPDATE sensor_data
SET well = 'Well 1'
WHERE well IS NULL
""")

connection.commit()

connection.close()

print("Database updated successfully!")


import mysql.connector
import os
import re

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'scobiform',
    'raise_on_warnings': True
}

# Remove colons and hashes using regex
def removeFromString(text):
    return re.sub(r"[:#]", "", text)

try:
    # Connect to MySQL
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Query posts
    query = "SELECT id, title, body, slug, created_at FROM posts"
    cursor.execute(query)

    output_dir = 'posts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through posts
    for (id, title, body, slug, created_at) in cursor:
        filename = f"{output_dir}/{slug}.md"

        # Clean strings
        slug = removeFromString(slug)
        title = removeFromString(title)

        # Write md files
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: {title}\ndate: {created_at}\ndescription: {title}\ntag: \nauthor: scobiform\n---\n{body}")

    print(f"Markdown files have been saved to {output_dir}/")

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as e:
    print(f"Error: {e}")

finally:
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()
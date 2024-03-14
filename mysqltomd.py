import mysql.connector
import os
import re

config = {
    'user': 'root', # Change this to your MySQL username
    'password': '', # Change this to your MySQL password
    'host': '127.0.0.1', # Change this to your MySQL server IP
    'database': 'scobiform', # Change this to your database name
    'raise_on_warnings': True
}

# Remove unwanted characters using regex
def removeFromString(text, max_length=210):
    text = re.sub(r'[:#""]', '', text)
    # Cut down the string
    max_length = max_length - len(output_dir) - len(".md") - 1 
    return text[:max_length]

# Function to convert basic HTML to Markdown
def html_to_markdown(html):
    # Convert headings
    for i in range(6, 0, -1):
        html = re.sub(f'<h{i}>(.*?)<\/h{i}>', f'{"#" * i} \\1', html)

    # Convert paragraphs
    html = re.sub('<p>(.*?)<\/p>', '\\1\n', html)

    # Convert links
    html = re.sub('<a href="(.*?)">(.*?)<\/a>', '[\\2](\\1)', html)

    # Convert strong/bold
    html = re.sub('<strong>(.*?)<\/strong>', '**\\1**', html)
    html = re.sub('<b>(.*?)<\/b>', '**\\1**', html)

    # Convert em/italic
    html = re.sub('<em>(.*?)<\/em>', '*\\1*', html)
    html = re.sub('<i>(.*?)<\/i>', '*\\1*', html)

    # Convert pre/code
    html = re.sub('<pre>(.*?)<\/pre>', '```\\1```', html)
    html = re.sub('<code>(.*?)<\/code>', '`\\1`', html)

    # Convert iframe to iframe shortcode
    html = re.sub('<iframe(.*?)src="(.*?)"(.*?)><\/iframe>', '<youtube youtubeLink="\\2"/>', html)

    return html

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
        # Clean strings
        slug = removeFromString(slug)
        title = removeFromString(title, 777)

        # Set filename
        filename = f"{output_dir}/{slug}.mdx"

        # Trim date
        created_at = created_at.strftime("%Y-%m-%d")

        # Convert HTML to Markdown
        body = html_to_markdown(body)

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
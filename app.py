import os, string
import markdown
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config.from_mapping(
    FLASK_ENV='development'
        )

@app.route('/')
def view_article():
    # Scan for file name
    filepath = scan_for_file('example.md')
    
    # Parse 
    md_conten = read_file_to_string(filepath)

    # Convert to HTML
    generated_html=  markdown.markdown(md_conten, extensions=['fenced_code'])

    # Separate HTML by <hr /> for card preparation
    cards = assign_cards(generated_html)
    return render_template('base-with-cards.html', cards=cards)

def scan_for_file(filename):
    search_path = 'articles'
    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

def read_file_to_string(filepath):
    with open(filepath, 'r') as reader:
        content = reader.read()
    return content

def assign_cards(content):
    soup = BeautifulSoup(content,'html.parser')

    first_hr = soup.hr

    next_elem = first_hr.next_sibling
    cards = []
    current_card = ""

    for elem in first_hr.next_siblings:
        current_card = current_card + str(elem)
        if elem.name == "hr" :
            cards.append(current_card)
            current_card = ""

    cards.append(current_card)

    return cards

if __name__ == "__main__":
    app.run(debug=True)

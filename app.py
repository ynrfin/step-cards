import os, string
import markdown
from flask import Flask, render_template, abort
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config.from_mapping(
    FLASK_ENV='development'
        )

@app.route('/<path:filepath>')
def view_article(filepath):
    # Scan for file name

    file_location = os.getcwd() + '/articles/' + filepath + ".md"
    file_location = "articles/" + filepath + ".md"
    if not os.path.exists(file_location):
        abort(404, "Article not Found")

    # Parse 
    md_conten = read_file_to_string(file_location)

    # Convert to HTML
    generated_html=  markdown.markdown(md_conten, extensions=['fenced_code'])

    # Separate HTML by <hr /> for card preparation
    cards = assign_cards(generated_html)
    return render_template('base-with-cards.html', cards=cards)

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

        if elem.name == "hr" :
            cards.append(current_card)
            current_card = ""
        else:
            current_card = current_card + str(elem)

    cards.append(current_card)

    return cards

if __name__ == "__main__":
    app.run(debug=True)

import os, string
import markdown
from flask import Flask, render_template, abort
from bs4 import BeautifulSoup
import pathlib

app = Flask(__name__)

app.config.from_mapping(
    FLASK_ENV='development'
        )

@app.route('/<path:filepath>')
def view_article(filepath):
    # Scan for file name

    file_location = os.getcwd() + '/articles/' + filepath + ".md"
    file_location = "articles/" + filepath
    if not os.path.exists(file_location):
        abort(404, "Article not Found")

    # Parse 
    md_conten = read_file_to_string(file_location)

    # Convert to HTML
    md = markdown.Markdown(
        extensions=['fenced_code', 'meta', 'codehilite'],
        extension_configs={
            'codehilite':{
                'noclasses':True,
                'pygments_style': 'solarizedlight'
                }
            }
        )
    generated_html = md.convert(md_conten)

    # set title of the article from Markdown metadata
    article_title = "-"
    if "title" in md.Meta:
        article_title = md.Meta['title'][0]

    # Separate HTML by <hr /> for card preparation
    cards = assign_cards(generated_html)

    articles = scan_available_articles('articles')
    return render_template('base-with-cards.html',
            article_title = article_title,
            cards=cards,
            articles_list=articles)

def read_file_to_string(filepath):
    with open(filepath, 'r') as reader:
        content = reader.read()
    return content

def assign_cards(content):
    soup = BeautifulSoup(content,'html.parser')

    first_h1 = soup.h1

    next_elem = first_h1.next_sibling
    cards = {}
    current_title = first_h1.string
    current_card = ""

    for elem in first_h1.next_siblings:
        if(elem.name == "h1"):
            cards[current_title] = current_card
            current_title = elem.string
            #cards[current_title] = ""
        else:
            current_card = current_card + str(elem)
        cards[current_title] = current_card

    return cards

def scan_available_articles(directory):
    """
    scan all files in the articles directory
    returns list of file's relative path
    """

    articles_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)

                p = pathlib.Path(filepath)
                filepath = pathlib.Path(*p.parts[1:])
                #print(p.parts[1:])
                articles_list.append(filepath)
    return articles_list

if __name__ == "__main__":
    app.run(debug=True)

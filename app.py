import os, string
import markdown
from flask import Flask

app = Flask(__name__)

app.config.from_mapping(
    FLASK_ENV='development'
        )

@app.route('/')
def view_article():
    # Scan for file name
    filepath = scan_for_file('example.md')
    
    # Parse 
    md_conten = parse_file_content(filepath)
    return markdown.markdown(md_conten, extensions=['fenced_code'])

def scan_for_file(filename):
    search_path = 'articles'
    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

def parse_file_content(filepath):
    with open(filepath, 'r') as reader:
        content = reader.read()
        print(content)
    return content

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search term from the form
        search_term = request.form.get('search_term')

        # Run the Scrapy spider with the search term
        subprocess.run(['scrapy', 'crawl', 'amazon', '-a', f'search_query={search_term}'])

        # Return the done.html template
        return render_template('done.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

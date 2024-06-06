from flask import render_template
from website import create_app


# Create a Flask Instance
app = create_app()


# Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(error):
    return render_template('error500.html'), 500


if __name__ == '__main__':
    # Only if we run this file not just import it, we execuㅅe the next line.
    app.run(debug=True)
    # Because in case we import main.py in another file, it would run the server.

from .models import User
from . import db

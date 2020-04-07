from flask import Flask

app = Flask(__name__)

# importing and register Blueprint. Connecting to the main app.
from caliweb.core.views import core
app.register_blueprint(core)

from caliweb.error_pages.handlers import error_pages
app.register_blueprint(error_pages)
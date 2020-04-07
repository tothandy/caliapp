from flask import Flask

app = Flask(__name__)

# importing and register Blueprint. 
from caliweb.core.views import core
app.register_blueprint(core)
from flask import Flask
import Config
from app.commands import create_files

app = Flask(__name__)
app.config.from_object(Config)

app.cli.add_command(create_files)

from app import routes
from flask import Blueprint


web = Blueprint('web', __name__, template_folder='templates',
                static_folder='dist')


from . import index

from flask import Flask, g, render_template, request, jsonify

import os
import sys
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deep_learning'))
from deep_learning.query import QueryManager


def create_app():
    app = Flask(__name__)

    qm = QueryManager()

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html')

    @app.errorhandler(500)
    def server_error(error):
        err_msg = str(error)
        return render_template('500.html', err_msg=err_msg), 500

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_go', methods=['POST'])
    def get_go():
        state = request.form.getlist('state[]')
        state = [int(s) for s in state]
        res = qm.query(state)
        ret = (res//15,res%15)

        return jsonify(ret)

    return app
import datetime
import json
import traceback
from flask import Blueprint, render_template, session, url_for, request, flash
from werkzeug.utils import redirect
from ..db import DAO
from app.Common import Token, RESULT, __TIMEOUT__SEC__, __TIMEOUT__DAY__, __OFFSET__
from app.logger import logger
from ..module import token_make, token_check
bp = Blueprint('test', __name__, url_prefix="/test")
PORT = ''
TOKEN = ''

@bp.route('/main')
def pageTestMain():
    port_list = ['']
    for i in range(1, 20):
        port_list.append(f'COM{i}')
    return render_template('test_main.html', port_list = port_list)

@bp.route('/start')
def testStart():
    try:
        port = request.args.get('port')
        global PORT ,TOKEN
        PORT = port
        scan = token_make.Scan(port)
        res = scan.run()
        logger.info(res)
        TOKEN = res['DATA']['token']
        return TOKEN
    except Exception as e:
        logger.error(e)
        print(traceback.format_exc())
        return e

@bp.route('/end')
def testEnd():
    result = '999'
    try:
        point = request.args.get('point')
        global TOKEN
        sp = str(TOKEN).split('$')
        id = sp[0]
        ex = sp[1]
        time = sp[2]
        res = token_check.check(id, point, ex, time)
        logger.info(res)
        result = res['RESULT']
    except Exception as e:
        logger.error(e)
        print(traceback.format_exc())
    finally:
        TOKEN = ''
        return result
import simplejson as json
from flask import Flask, request, Response, redirect, render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'HeightWeight'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Abhay Patel'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM HW')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, hw=result)


@app.route('/view/<int:hw_id>', methods=['GET'])
def detail_view(hw_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM HW WHERE id=%s', hw_id)
    result = cursor.fetchall()
    return render_template('view.html', title='Detail View', hw=result[0])


@app.route('/edit/<int:hw_id>', methods=['GET'])
def edit_record(hw_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM HW WHERE id=%s', hw_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Record', hw=result[0])


@app.route('/edit/<int:hw_id>', methods=['POST'])
def update_record(hw_id):
    cursor = mysql.get_db().cursor()
    requestData = (request.form.get('height'), request.form.get('weight'), hw_id)
    sql_update_query = """UPDATE HW t SET t.height = %s, t.weight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, requestData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/new', methods=['GET'])
def create_record():
    return render_template('new.html', title='Create New Record')


@app.route('/new', methods=['POST'])
def insert_record():
    cursor = mysql.get_db().cursor()
    requestData = (request.form.get('height'), request.form.get('weight'))
    sql_insert_query = """INSERT INTO HW (`height`,`weight`) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, requestData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:hw_id>', methods=['POST'])
def delete_record(hw_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM HW WHERE id = %s """
    cursor.execute(sql_delete_query, hw_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/hw', methods=['GET'])
def api_getAll() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM HW')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/hw/<int:hw_id>', methods=['GET'])
def api_getRow(hw_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM HW WHERE id=%s', hw_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/hw/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/hw/<int:hw_id>', methods=['PUT'])
def api_edit(hw_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/hw/<int:hw_id>', methods=['DELETE'])
def api_delete(hw_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
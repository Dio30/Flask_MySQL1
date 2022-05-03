from flask import Flask, flash, render_template,request,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'Dione'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "Dione"
app.config['MYSQL_PASSWORD'] = "98098694"
app.config['MYSQL_DB'] = "minha_base_de_dados"
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM jogos")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', jogo=data)

@app.route("/inserir", methods = ["POST"])
def inserir():
    if request.method == "POST":
        details = request.form
        flash("Jogo inserido com sucesso")
        nome = details['nome']
        ano_lançamento = details['ano_lançamento']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO jogos(nome, ano_lançamento) VALUES (%s,%s)", (nome, ano_lançamento,))
        mysql.connection.commit()
        return redirect(url_for("Index"))

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        flash("Jogo foi atualizado com sucesso")
        id_data = request.form['id']
        name = request.form['nome']
        ano_lançamento = request.form['ano_lançamento']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE jogos
            SET nome=%s, ano_lançamento=%s
            WHERE id=%s
            """, (name, ano_lançamento, id_data,))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route("/delete/<string:id_data>", methods = ["GET"])
def delete(id_data):
    flash("Jogo foi deletado com sucesso")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM jogos WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)
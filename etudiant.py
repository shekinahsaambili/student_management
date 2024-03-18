from flask import Flask, render_template, request, redirect
import mysql.connector
import fun


app = Flask(__name__)

# Configuration de la base de données MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crudtp"
)

# Page d'accueil pour afficher les éléments
@app.route('/')
def home():
    return render_template('login.html')

    
# Page pour supprimer un élément
@app.route('/delete/<matricule>/')
def delete(matricule):
    cursor = db.cursor()
    cursor.execute("DELETE FROM etudiant WHERE matricule=%s", (matricule,))
    cursor.execute("DELETE FROM utilisateur WHERE password=%s", (matricule,))
    db.commit()
    return redirect('/index')

# Page pour changer les coordonnées d'un élément
@app.route('/update/<matricule>/', methods=['POST'])
def update(matricule):
    if request.method=='POST':
        nom = request.form['nom']
        postnom= request.form['postnom']
        cursor = db.cursor()
        req="UPDATE etwudiant SET nom=%s, postnom=%s  WHERE matricule=%s"
        valeur=(nom,postnom, matricule,)
        cursor.execute(req, valeur)
        db.commit()
        return redirect('/index')

@app.route('/lancer_update/<matricule>/')
def lancer_update(matricule):
    req= "SELECT*FROM etudiant WHERE matricule = %s"
    cur=db.cursor()
    cur.execute(req,(matricule,))
    data= cur.fetchall()

    return render_template('update.html', data=data)

# Page pour enregistrer les données
@app.route('/save', methods=['POST'])
def save():
    if request.method=='POST':
        
        nom=fun.rsa(request.form['nom'],int(request.form['n']),int(request.form['e']))
        postnom=fun.rsa(request.form['postnom'],int(request.form['n']),int(request.form['e']))
        # print("messahe est",matricule)
        cursor = db.cursor()
        sql="INSERT INTO etudiant(nom,postnom,matricule) VALUES(%s,%s,%s)"
        cursor.execute(sql,(nom,postnom,request.form['matricule']))
        sql1='INSERT INTO utilisateur(username,password,e,n) VALUES (%s,%s,%s,%s)'
        cursor.execute(sql1,(request.form['nom']+request.form['postnom'],request.form['matricule'],request.form['e'],request.form['n']))
        db.commit()
        
        return redirect('/index')
    
    
@app.route('/appel', methods=['GET'])
def appel():
    return render_template('etudiant.html')


@app.route('/index')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM etudiant")
    elements = cursor.fetchall()
    return render_template('index.html', elements=elements)


# Page de connexion
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur = db.cursor()
    cur.execute("SELECT * FROM utilisateur WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    

    if user:
        
        cur.execute("SELECT * FROM etudiant")
        elements = cur.fetchall()
        
        return redirect('/index')

    else:
        return redirect('/')





if __name__ == '__main__':
    app.run(debug=True)



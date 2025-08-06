from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///phonebook.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Phone(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name} - {self.phone_number}"


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        phone = Phone(name=name, phone_number=phone_number)
        db.session.add(phone)
        db.session.commit()
        
    allPhone = Phone.query.all()
    return render_template('index.html', allPhone=allPhone)

@app.route("/phonenumber")
def saved_phone_numbers():
    allPhone = Phone.query.all()
    return render_template('saves.html', allPhone=allPhone)

@app.route("/delete/<int:sno>")
def delete(sno):
    phone = Phone.query.filter_by(sno=sno).first()
    db.session.delete(phone)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
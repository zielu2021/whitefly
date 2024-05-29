from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.id}>"

@app.route('/')
def index():
    # return "Welcome in Flask"
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        user_data = request.form['data']
        new_user = User(data=user_data)
        db.session.add(new_user)
        db.session.commit()
        # return "Data saved!"
        return '''Data saved! <a href="/">Back to index</a>'''
    return render_template('form.html')

@app.route('/async-form-page')
def async_form_page():
    return render_template('async_form.html')
"""This route serves the HTML template that includes the asynchronous form."""

@app.route('/async-form', methods=['POST'])
def async_form():
    user_data = request.json['data']
    new_user = User(data=user_data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Data saved asynchronously!'})
"""This route is used to handle the AJAX POST request from the form. 
It does not serve a page but responds with JSON data about the outcome of the form submission"""

@app.route('/last_record')
def last_record():
    record = User.query.order_by(User.id.desc()).first()
    if record:
        return jsonify({
            "id": record.id,
            "data": record.data
        })
    else:
        return jsonify({"error": "No records found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

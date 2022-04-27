from flask import current_app as app, session, request, jsonify, abort
from datetime import timedelta
from flask_login import login_required, logout_user, current_user, login_user
from taxpayer import db, bcrypt
from taxpayer.models import Accountant, TaxPayer


@app.route('/')
@app.route('/home')
def home():
    taxPayers = TaxPayer.query.all()
    count = 0
    txPayers = {}
    for payer in taxPayers:
        newObj = {"first name": payer.firstName, "last name": payer.lastName,
                  "email": payer.email, "state": payer.state, "phone number": payer.phoneNumber, "accountant": f"{payer.accountant.firstName} {payer.accountant.lastName}"
                  }

        count += 1
        txPayers[f"Payer{count}"] = newObj
    return txPayers


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=2)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form['remember']
        accountant = Accountant.query.filter_by(
            username=username).first()

        if accountant and bcrypt.check_password_hash(accountant.password, password):
            login_user(accountant, remember=remember)

        return jsonify("Successful")

    return jsonify({'example': {'username': 'Your Username', 'password': 'Your Password', 'remember': 'True or False'}})


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return jsonify({"username": current_user.username})

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['first name']
        lastName = request.form['last name']
        email = request.form['email']
        phoneNumber = request.form['phone number']
        hashed_password = bcrypt.generate_password_hash(
            password=password).decode('utf-8')

        accountant = Accountant(username=username, email=email, password=hashed_password,
                                firstName=firstName, lastName=lastName, phoneNumber=phoneNumber)

        db.session.add(accountant)
        db.session.commit()

        return jsonify("Successful")

    return jsonify({'example': {'username': 'Your Username',
                                'password': 'Your Password',
                                'first name': 'Your FirstName',
                                'last name': 'Your LastName',
                                'email': 'Your Email',
                                'phone number': 'Your PhoneNumber'}
                    }
                   )


@app.route('/accountants', methods=['POST', 'GET'])
@login_required
def accountants():
    accontants = Accountant.query.order_by(Accountant.date_created.desc()).all()
    count = 0
    txPayers = {}
    for accountant in accontants:
        newObj = {"first name": accountant.firstName, "last name": accountant.lastName,
                  "email": accountant.email, "phone number": accountant.phoneNumber
                  }

        count += 1
        txPayers[f"Accountant{count}"] = newObj
    return txPayers


@app.route('/payers', methods=['POST', 'GET'])
@login_required
def payers():
    if request.method == 'POST':
        firstName = request.form['first name']
        lastName = request.form['last name']
        email = request.form['email']
        state = request.form['state']
        phoneNumber = request.form['phone number']

        taxpayer = TaxPayer(firstName=firstName, lastName=lastName,
                            email=email, state=state, phoneNumber=phoneNumber, user_id=current_user.id)

        db.session.add(taxpayer)
        db.session.commit()

        return jsonify("Successful")

    return jsonify({'example':
                        {'first name': 'Payer First Name',
                         'last name': 'Payer Last Name',
                         'email': 'Payer Email',
                         'state': 'Payer State',
                         'phone number': 'Payer Phone Number'
                         }
                        })


@app.route('/payers/<int:payer_id>', methods=['POST', 'GET'])
@login_required
def editPayer(payer_id):
    payer = TaxPayer.query.get_or_404(payer_id)
    # if payer:
    #     print(payer)
    #     return jsonify("Successful")
    if request.method == 'POST':
        payer.firstName = request.form['first name']
        payer.lastName = request.form['last name']
        payer.email = request.form['email']
        payer.state = request.form['state']
        payer.phoneNumber = request.form['phone number']

        db.session.commit()

        return jsonify("Successful")

    myObj = {"first name": payer.firstName, "last name": payer.lastName,
                  "email": payer.email, "state": payer.state, "phone number": payer.phoneNumber
                  }

    return myObj

@app.route('/payers/<int:payer_id>/delete', methods=['POST', 'GET'])
@login_required
def deletePayer(payer_id):
    payer = TaxPayer.query.get_or_404(payer_id)
    if payer.accountant != current_user:
        abort(404)

    db.session.delete(payer)
    db.session.commit()
    return jsonify("Successful")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify('You have logged out successfully')

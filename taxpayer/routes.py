from flask import current_app as app, session, request, jsonify, abort
from datetime import timedelta, datetime
from flask_login import login_required, logout_user, current_user, login_user
from taxpayer import db, bcrypt
from taxpayer.models import Accountant, TaxPayer
from taxpayer.utils import Tax, getDiff, getDate


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
    accontants = Accountant.query.order_by(
        Accountant.date_created.desc()).all()
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
        salary = request.form['salary']

        taxpayer = TaxPayer(firstName=firstName, lastName=lastName,
                            email=email, state=state, phoneNumber=phoneNumber, salary=salary, user_id=current_user.id)

        db.session.add(taxpayer)
        db.session.commit()

        return jsonify("Successful")

    return jsonify({'example':
                    {'first name': 'Payer First Name',
                     'last name': 'Payer Last Name',
                     'email': 'Payer Email',
                     'state': 'Payer State',
                     'phone number': 'Payer Phone Number',
                     'salary': 'Payer Annual Salary'
                     }
                    })


@app.route('/payers/<int:payer_id>')
@login_required
def viewpayers(payer_id):
    payer = TaxPayer.query.get_or_404(payer_id)
    dueDate1 = getDate(days=365, date1=payer.datePaid)
    myObj = {"first name": payer.firstName, "last name": payer.lastName,
             "email": payer.email, "state": payer.state, "phone number": payer.phoneNumber, "salary": payer.salary, "status": payer.status,
             "When Due": dueDate1
             }

    return myObj


@app.route('/payers/<int:payer_id>/taxpayable', methods=['POST', 'GET'])
@login_required
def taxpayable(payer_id):
    payer = TaxPayer.query.get_or_404(payer_id)

    if request.method == 'POST':
        stateTax = int(request.form["state tax"] if not None else 0)
        arrears = int(request.form["arrears"] if not None else 0)
        fines = int(request.form["fines"] if not None else 0)
        payable = Tax(annualsalary=payer.salary,
                      stateTax=stateTax, arrears=arrears, fines=fines)

        dueDate = getDiff(date1=payer.datePaid)
        dueDate1 = dueDate // 365
        if dueDate1 >= 0:
            dateToPay = getDate(days=dueDate)
            payer.yearsOwned = dueDate1
            return jsonify({"Tax Payable": f"{payable.taxPayable()}", "Date Due": dateToPay})

        return jsonify(f"{payable.taxPayable()}")

    return jsonify({"Pay Tax": {
        "state tax": "Payer State Tax",
        "fines": "Payer Fines",
        "arrears": "Payer Arrears"
    }
    })


@app.route('/payers/<int:payer_id>/paytax', methods=['POST', 'GET'])
def paytax(payer_id):
    payer = TaxPayer.query.get_or_404(payer_id)
    if payer.status == 'Paid':
        return jsonify("This payer is ahead of his tax")

    elif payer.status == 'Delayed':
        if request.method == 'POST':
            card = request.form["card"]
            expiryDate = request.form["expiry date"]
            cvc = request.form["cvc"]

            # This logic is meant to use the card inputted and use it to pay for the tax

            ##
            payer.status = 'Paid'
            payer.datePaid = datetime.utcnow
            return jsonify("Successful")

        return jsonify({
            "to do": f"Update fines, state tax and arrears of payer before moving on. You also need to pay your taxes, you are behind by {payer.yearsOwned}. To pay, enter your card details below.",
            "card": "16 digit number.",
            "expiry date": "In the format 'M/Y'.",
            "cvc": "This can be found at the back of your card."
        })


@app.route('/payers/<int:payer_id>/tax/status')
@login_required
def tax(payer_id):
    payer = TaxPayer.query.get_or_404(payer_id)
    dueDate = getDiff(date1=payer.datePaid)
    dueDate1 = dueDate // 365
    if dueDate1 > 0:
        payer.yearsOwned = dueDate1
        payer.status = 'Delayed'

    return jsonify({"status": payer.status})


@app.route('/payers/<int:payer_id>/edit', methods=['POST', 'GET'])
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
        payer.annualSalary = request.form['salary']

        db.session.commit()

        return jsonify("Successful")

    myObj = {"first name": "Payer First Name", "last name": "Payer Last Name",
             "email": "Payer State", "state": "Payer State", "phone number": "Payer Phone Number", "salary": "Payer Annual Salary"
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

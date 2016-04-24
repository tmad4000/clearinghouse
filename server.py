import os
from flask import Flask, render_template, request
import stripe
    # 'secret_key': os.environ['SECRET_KEY'],
    # 'publishable_key': os.environ['PUBLISHABLE_KEY']


stripe_keys = {
    'secret_key': 'asdf',
    'publishable_key': 'asdf'
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge_republican', methods=['POST'])
def charge_republican():
    amount = 500
    current = 'usd'

    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='republican'
    )

    return render_template('charge.html', amount=amount)

@app.route('/charge_democrat', methods=['POST'])
def charge_democratic():
    amount = request.args.get('amount')
    current = 'usd'

    customer = stripe.Customer.create(
        email='customer@example.com',
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='democrat'
    )

    return render_template('charge.html', amount=amount)


@app.route('/total_donations')
def total_donations():
    party = request.args.get('party')
    stripe.api_key = "sk_test_KRAa3eTpGkrw56mzIhFwSwyG"
    charges = stripe.Charge.all()['data']
    total_amount = 0
    for charge in charges:
        if charge['description'] == party:
            total_amount += charge['amount']
    return render_template('total.html', total_amount=total_amount)

if __name__ == '__main__':
    app.run(debug=True)

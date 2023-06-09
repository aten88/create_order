import random

from binance.client import Client

from flask import Flask, request, jsonify

app = Flask(__name__)

app.config.from_pyfile('secrets.cfg', silent=True)


def create_orders(data):

    client = Client(app.config['API_KEY'], app.config['SECRET_KEY'])

    volume = data['volume']
    number = data['number']
    amount_dif = data['amountDif']
    side = data['side']
    price_min = data['priceMin']
    price_max = data['priceMax']

    orders = []

    for _ in range(number):
        price = random.uniform(price_min, price_max)

        amount = random.uniform(
            volume/number - amount_dif,
            volume/number + amount_dif
        )

        if side == 'SELL':
            order = client.create_order(
                symbol='BTCUSDT',
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=amount,
                price=price
            )
        elif side == 'BUY':
            order = client.create_order(
                symbol='BTCUSDT',
                side='BUY',
                type='LIMIT',
                timeInForce='GTC',
                quantity=amount,
                price=price
            )

        orders.append(order)
    return orders


@app.route('/create_orders', methods=['POST'])
def create_orders_endpoint():
    try:
        data = request.get_json()

        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid data format'})

        orders = create_orders(data)

        return jsonify({'orders': orders})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run()

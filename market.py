from flask import Flask, render_template, session, redirect, url_for
import data
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
dat = data.data

@app.route("/")
def homepage():
    arr = ['home.html', 'product.html']
    message = session.pop('message', None) 
    return render_template(arr, data=dat)

@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    item = next((item for item in dat if item['id'] == item_id), None)
    
    if item:
        cart = session.get('cart', [])
        cart.append(item)
        session['cart'] = cart
        session['message'] = f"{item['name']} added to cart" 
        time.sleep(1) 
        return redirect(url_for('homepage'))
    else:
        return "Item not found", 404
    
@app.route("/remove_from_cart/<int:item_id>", methods=['POST'])
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    
    for item in cart:
        if item['id'] == item_id:
            cart.remove(item)
            break
    
    session['cart'] = cart
    return redirect(url_for('cart'))



@app.route("/cart")
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

if __name__ == "__main__":
    app.run(debug=True)

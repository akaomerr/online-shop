from flask import Flask, render_template, redirect, request
import csv,os
from dotenv import load_dotenv



env_path=os.path.join(os.path.dirname(__file__),'static','secrets.env')
load_dotenv(env_path)
secret_key=os.getenv('ADDITEMPW')
csv_path = os.path.join(os.path.dirname(__file__), 'templates', 'products.csv')
app = Flask(__name__)

check_cart=0

cart_csv_path=os.path.join(os.path.dirname(__file__), 'templates', 'cart.csv')
with open(csv_path, 'r') as file:
    lines = file.readlines()
    product_id = len(lines)

@app.route("/")
def index():
    global check_cart
    if check_cart!=0:
        add_cart=True
        check_cart=0
    else:
        add_cart=False
    products = []
    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            products.append({
                'product_name': row[0],
                'product_price': row[1],
                'product_description': row[2],
                'product_image': row[3],
                'product_id':row[4]
            })
    return render_template('index.html', products=products,add_cart=add_cart)

@app.route("/add_product", methods=['GET', 'POST'])
def addproduct():
    global product_id
    admin_password=request.form.get('admin_password')
    if request.method == 'POST':
        if admin_password==secret_key:
            product_id+=1
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            product_description = request.form.get('product_description')
            product_image = request.form.get('product_image')

            with open(csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([product_name, product_price, product_description, product_image,product_id])

            return redirect('/')
        else:
            admin_password_check=False
            return render_template('addproduct.html',admin_password_check=admin_password_check)
    return render_template('addproduct.html')

@app.route("/add_to_cart/<product_name>/<product_price>/<product_id>", methods=['POST'])
def add_to_cart(product_name, product_price,product_id):
    global check_cart
    if request.method=="POST":
        check_cart+=1
    if not os.path.exists(cart_csv_path):
        with open(cart_csv_path, mode='w', newline='') as cart_file:
            cart_writer = csv.writer(cart_file)
            cart_writer.writerow(['Product Name', 'Product Price','Product ID'])

    with open(cart_csv_path, mode='a', newline='') as cart_file:
        cart_writer = csv.writer(cart_file)
        cart_writer.writerow([product_name, product_price,product_id])
    
    return redirect('/')

@app.route("/cart")
def cart():
    products = []
    total_coast=0
    with open(cart_csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            products.append({
                'product_name': row[0],
                'product_price': row[1],
                'product_id':row[2]
            })
            total_coast+=int(row[1])
    return render_template('cart.html', products=products, total_coast=total_coast)

@app.route('/deleted_product/<int:product_id>')
def deleted_product(product_id):
    
    with open(cart_csv_path,'r') as file:
        reader=csv.reader(file)
        rows=list(reader)
    for row in rows:
        print(row[2])
        if int(row[2])==product_id:
            rows.remove(row)
            break
    with open(cart_csv_path,'w',newline='') as file:
        writer=csv.writer(file)
        writer.writerows(rows)

    return redirect('/cart')

@app.route('/payment')
def payment():

    return render_template('payment.html')

if __name__ == "__main__":
    app.run(debug=True)
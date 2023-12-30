from flask import Flask, render_template, redirect, request
import csv,os
from dotenv import load_dotenv
env_path=os.path.join(os.path.dirname(__file__),'static','secrets.env')
load_dotenv(env_path)
secret_key=os.getenv('ADDITEMPW')
csv_path = os.path.join(os.path.dirname(__file__), 'templates', 'products.csv')
app = Flask(__name__)

@app.route("/")
def index():
    products = []
    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            products.append({
                'product_name': row[0],
                'product_price': row[1],
                'product_description': row[2],
                'product_image': row[3]
            })
    return render_template('index.html', products=products)

@app.route("/add_product", methods=['GET', 'POST'])
def addproduct():
    admin_password=request.form.get('admin_password')
    if request.method == 'POST':
        if admin_password==secret_key:
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            product_description = request.form.get('product_description')
            product_image = request.form.get('product_image')

            with open(csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([product_name, product_price, product_description, product_image])

            return redirect('/')
        else:
            admin_password_check=False
            return render_template('addproduct.html',admin_password_check=admin_password_check)
    return render_template('addproduct.html')

if __name__ == "__main__":
    app.run(debug=True)
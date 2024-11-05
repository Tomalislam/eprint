from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from PyPDF2 import PdfReader
from flask_sqlalchemy import SQLAlchemy
import os
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a proper secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'  # Change this to your database URI
db = SQLAlchemy(app)

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(255))
    total_price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Price settings
PRICES = {
    'A4': {'color': 3.0, 'black_and_white': 1.5},
    'A5': {'color': 1.5, 'black_and_white': 0.8}
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'file_details' not in session:
        session['file_details'] = []  # Initialize session
    
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        page_size = request.form.get('page_size')
        color_type = request.form.get('color_type')
        
        file_details = session['file_details']
        for file in files:
            if file.filename != '' and not any(f['filename'] == file.filename for f in file_details):  # Check for duplicates
                reader = PdfReader(file)
                num_pages = len(reader.pages)

                if page_size in PRICES and color_type in PRICES[page_size]:
                    price_per_page = PRICES[page_size][color_type]
                    file_price = num_pages * price_per_page

                    file_details.append({
                        'filename': file.filename,
                        'total_pages': num_pages,
                        'page_size': page_size,
                        'color_type': color_type,
                        'price': file_price
                    })

        session['file_details'] = file_details  # Update session

    total_price = sum(file['price'] for file in session['file_details'])
    return render_template('index.html', file_details=session.get('file_details', []), total_price=total_price)

@app.route('/clear', methods=['POST'])
def clear_files():
    session.pop('file_details', None)  # Clear session data
    return redirect(url_for('home'))
    
@app.route('/order', methods=['GET'])
def order():
    file_details = session.get('file_details', [])
    total_price = sum(file['price'] for file in file_details)
    return render_template('order.html', file_details=file_details, total_price=total_price)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    
    total_price = sum(file['price'] for file in session.get('file_details', []))

    # Create a new Order instance
    new_order = Order(name=name, email=email, phone=phone, address=address, total_price=total_price)
    
    # Add the order to the session and commit to the database
    db.session.add(new_order)
    db.session.commit()

    # Send an email notification
    send_order_email(new_order)

    return render_template('confirmation.html', name=name, email=email, phone=phone, address=address)

@app.route('/order_summary', methods=['GET'])
def order_summary():
    orders = Order.query.all()  # Retrieve all orders from the database
    return render_template('order_summary.html', orders=orders)

def send_order_email(order):
    msg = MIMEText(f"New order received:\n\nName: {order.name}\nEmail: {order.email}\nPhone: {order.phone}\nAddress: {order.address}\nTotal Price: {order.total_price}")
    msg['Subject'] = 'New Order Received'
    msg['From'] = 'lisulislamtomal@gmail.com'  # Use your email
    msg['To'] = 'lisulislamtomal@gmail.com'  # Send it to yourself

    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Use your SMTP server
        server.starttls()
        server.login('lisulislamtomal@gmail.com', 'acla uqyu dgvu uull')  # Use your actual email and password
        server.send_message(msg)

if __name__ == '__main__':
    db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)

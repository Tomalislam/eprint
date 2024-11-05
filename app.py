from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from PyPDF2 import PdfReader
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for storing orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    page_size = db.Column(db.String(10), nullable=False)
    color_type = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

# Price configuration
PRICES = {
    'A4': {
        'color': 3.0,
        'black_and_white': 1.5
    },
    'A5': {
        'color': 1.5,
        'black_and_white': 0.8
    }
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'file_details' not in session:
        session['file_details'] = []
    
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        page_size = request.form.get('page_size')
        color_type = request.form.get('color_type')

        file_details = session['file_details']
        for file in files:
            if file.filename and not any(f['filename'] == file.filename for f in file_details):
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

        session['file_details'] = file_details

    total_price = sum(file['price'] for file in session.get('file_details', []))
    return render_template('index.html', file_details=session.get('file_details', []), total_price=total_price)

@app.route('/clear', methods=['POST'])
def clear_files():
    session.pop('file_details', None)
    return redirect(url_for('home'))

@app.route('/order', methods=['GET', 'POST'])
def order():
    file_details = session.get('file_details', [])
    if request.method == 'POST':
        customer_name = request.form.get('name')
        customer_email = request.form.get('email')
        phone_number = request.form.get('phone')

        if not file_details:
            flash('No files to order', 'danger')
            return redirect(url_for('home'))

        total_price = sum(file['price'] for file in file_details)

        for file in file_details:
            order = Order(
                filename=file['filename'],
                total_pages=file['total_pages'],
                page_size=file['page_size'],
                color_type=file['color_type'],
                price=file['price'],
                customer_name=customer_name,
                customer_email=customer_email,
                phone_number=phone_number
            )
            db.session.add(order)
        db.session.commit()

        # Send order confirmation email
        send_order_email(customer_name, customer_email, total_price, file_details)

        session.pop('file_details', None)
        return render_template('confirmation.html', name=customer_name, email=customer_email, phone=phone_number)

    total_price = sum(file['price'] for file in file_details)
    return render_template('order.html', file_details=file_details, total_price=total_price)

@app.route('/order_summary', methods=['GET'])
def order_summary():
    orders = Order.query.all()
    return render_template('order_summary.html', orders=orders)

def send_order_email(name, email, total_price, file_details):
    sender_email = os.getenv('EMAIL_USER')
    sender_password = os.getenv('EMAIL_PASS')
    receiver_email = email

    subject = 'Order Confirmation'
    body = f'Dear {name},\n\nThank you for your order. Here is your order summary:\n\n'
    for file in file_details:
        body += f"Filename: {file['filename']}, Pages: {file['total_pages']}, Price: {file['price']} TK\n"
    body += f"\nTotal Price: {total_price} TK\n\nBest regards,\nYour Company"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f'Failed to send email: {e}')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template, session, redirect, url_for
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Price per page configuration
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
        session['file_details'] = []  # Initialize session if not set
    
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        page_size = request.form.get('page_size')
        color_type = request.form.get('color_type')
        
        file_details = session['file_details']
        for file in files:
            if file.filename and not any(f['filename'] == file.filename for f in file_details):  # Check for duplicate files
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
    # Here you can process the order (like saving to database or sending an email)
    
    # After submitting the order, redirect to confirmation page
    return render_template('confirmation.html', name=name, email=email, phone=phone, address=address)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader

app = Flask(__name__)

# প্রতি পৃষ্ঠার মূল্য নির্ধারণ
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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    files = request.files.getlist('files[]')  # একাধিক ফাইল লিস্ট হিসেবে গ্রহণ
    page_size = request.form.get('page_size')  # 'A4' বা 'A5'
    color_type = request.form.get('color_type')  # 'color' বা 'black_and_white'

    total_pages = 0
    total_price = 0.0
    file_details = []

    for file in files:
        if file.filename != '':  # ফাইলটি খালি নয় কিনা তা যাচাই
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            total_pages += num_pages

            if page_size in PRICES and color_type in PRICES[page_size]:
                price_per_page = PRICES[page_size][color_type]
                file_price = num_pages * price_per_page
                total_price += file_price

                file_details.append({
                    'filename': file.filename,
                    'total_pages': num_pages,
                    'price': file_price
                })

    if total_pages == 0:
        return jsonify({'error': 'No valid PDF files uploaded'}), 400

    return jsonify({
        'total_pages': total_pages,
        'total_price': total_price,
        'file_details': file_details
    })

if __name__ == '__main__':
    app.run(debug=True)

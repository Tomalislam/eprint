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
    file = request.files['file']
    page_size = request.form.get('page_size')  # 'A4' বা 'A5'
    color_type = request.form.get('color_type')  # 'color' বা 'black_and_white'

    reader = PdfReader(file)
    num_pages = len(reader.pages)

    if page_size in PRICES and color_type in PRICES[page_size]:
        price_per_page = PRICES[page_size][color_type]
        total_price = num_pages * price_per_page
        return jsonify({
            'total_pages': num_pages,
            'price_per_page': price_per_page,
            'total_price': total_price
        })
    else:
        return jsonify({'error': 'Invalid page size or color type'}), 400

if __name__ == '__main__':
    app.run(debug=True)

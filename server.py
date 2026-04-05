from flask import Flask, request, jsonify
from flask_cors import CORS
import csv, os

app = Flask(__name__)
CORS(app)

CSV_FILE = os.path.join(os.path.dirname(__file__), 'italian_products.csv')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # ✅ Test route in browser
    if request.method == 'GET':
        return "Server is working ✅"

    # ✅ Get cart from frontend
    order = request.json or {}

    # Normalize order keys (lowercase for safety)
    order = {k.strip().lower(): int(v) for k, v in order.items()}

    rows = []
    fieldnames = []

    # ✅ Detect delimiter automatically (comma OR tab)
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        sample = f.read(1024)
        f.seek(0)

        dialect = csv.Sniffer().sniff(sample, delimiters=",\t")
        reader = csv.DictReader(f, dialect=dialect)
        fieldnames = reader.fieldnames

        for row in reader:
            name = row['name'].strip().lower()

            if name in order:
                current = int(row['stock'])
                row['stock'] = str(max(0, current - order[name]))

            rows.append(row)

    # ✅ Write updated stock back
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=dialect.delimiter)
        writer.writeheader()
        writer.writerows(rows)

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
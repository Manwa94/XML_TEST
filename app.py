from flask import Flask
from account import AccountProcessor

app = Flask(__name__)
processor = AccountProcessor("Input.xml")

@app.route("/generate_response", methods=["GET", "POST"])
def generate_response():
    transactions = processor.parse_xml_file()
    receipt_transactions = processor.filter_receipt_transactions(transactions)
    processor.create_response_spreadsheet(receipt_transactions)
    return "Response generated successfully", 200


if __name__ == "__main__":
    app.run(debug=True)

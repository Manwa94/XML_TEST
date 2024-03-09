from flask import Flask, request
from account import AccountProcessor

app = Flask(__name__)
processor = AccountProcessor('input.xml')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    #This code will upload input.xml file by POST Method
    transactions = processor.parse_xml_file()
    receipt_transactions = processor.filter_receipt_transactions(transactions)
    processor.create_response_spreadsheet(receipt_transactions)
    return 'Response generated successfully', 200

if __name__ == "__main__":
    app.run(debug=True)

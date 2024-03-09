import xmltodict
import pandas as pd

class AccountProcessor:
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def parse_xml_file(self):
        with open(self.xml_file) as file:
            xml_data = file.read()
        return xmltodict.parse(xml_data)

    def filter_receipt_transactions(self, transactions):
        receipt_transactions = []
        transactions = (transactions.get("ENVELOPE", {}).get("BODY",{}).get("IMPORTDATA",{}).get("REQUESTDATA",{}).get("TALLYMESSAGE",{})) 
        for transaction in transactions:
            # We can Only include "Receipt" transaction here
            if transaction.get("VOUCHER", {}).get("@VCHTYPE") == "Receipt":
                receipt_transactions.append(transaction)
        return receipt_transactions

    def create_response_spreadsheet(self, transactions):
        headers = [ "Transaction Type", "Vch No.", "Ref No.", "Ref Type", "Ref Date", "Debtor and Particulars", "Ref Amount", "Amount", "Amount Verified" ]
        data = []

        for transaction in transactions:
            transaction = transaction.get("VOUCHER", {})
            # Extracting data for each column
            row = [
                transaction.get("@VCHTYPE", "NA"),
                transaction.get("VOUCHERNUMBER", "NA"),
                transaction.get("REFERENCE", "NA"),
                transaction.get("REFERENCETYPE", "NA"),
                transaction.get("REFERENCEDATE", "NA"),
                transaction.get("PARTYLEDGERNAME", "NA"),
                transaction.get("ALLLEDGERENTRIES.LIST.1.AMOUNT","NA"),
                transaction.get("AMOUNT", "NA"),
                "Yes" if transaction.get("@AMOUNT", 0) == transaction.get("ALLLEDGERENTRIES.LIST.1.AMOUNT", 0) else "No"
            ]
            data.append(row)
        df = pd.DataFrame(data, columns=headers)
        df.to_excel("resultant_file.xlsx", index=False)

if __name__ == "__main__":
    input_xml_file = 'input.xml'
    processor = AccountProcessor(input_xml_file)
    parsed_data = processor.parse_xml_file()
    receipt_transactions = processor.filter_receipt_transactions(parsed_data)

    # Create response spreadsheet
    processor.create_response_spreadsheet(receipt_transactions)

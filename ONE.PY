import re
import pytesseract
from PIL import Image
import nltk
from flask import Flask, request, jsonify

nltk.download('punkt')

app = Flask(__name__)
@app.route('/')
def main():
    return "Delulu"

@app.route('/process_image', methods=['GET'])
def process_image():
    image = Image.open("C:/Users/khush/Downloads/IMAGE/Screenshot 2023-10-15 071210.jpg")


    extracted_text = pytesseract.image_to_string(image)
    words = nltk.word_tokenize(extracted_text)

    ticket_number_pattern = r'\b\d{12}\b'
    traveller_name_pattern = r'Mr\.\s*([A-Za-z\s]+)'
    ticket_number_match = re.search(ticket_number_pattern, extracted_text)
    traveller_name_match = re.search(traveller_name_pattern, extracted_text)
    ticket_number = ticket_number_match.group() if ticket_number_match else None
    traveller_name = traveller_name_match.group(1) if traveller_name_match else None

    pnr_pattern = r'AIRLINE PNR TICKET NO\.\s*([\w\d, ]+)'
    pnr_matches = re.findall(pnr_pattern, extracted_text)
    pnr_list = [pnr.strip() for pnr in pnr_matches[0].split(',')]

    response = {
        "Tokenized Words": words,
        "Traveller Name": traveller_name,
        "Ticket Number": ticket_number,
        "PNR List": pnr_list
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

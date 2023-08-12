import xml.etree.ElementTree as ET
import re
import datetime
import locale
from collections import defaultdict
from bidi.algorithm import get_display
from persian_reshaper import reshape
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def format_unix_timestamp_year_month(timestamp_ms):
    timestamp_sec = timestamp_ms / 1000.0  # Convert milliseconds to seconds
    date = datetime.datetime.fromtimestamp(timestamp_sec)
    formatted_date = date.strftime("%Y-%m")
    return formatted_date

def extract_sms_data(xml_file):

    sms_data_list = []

    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_data = f.read()

    root = ET.fromstring('<root>' + xml_data + '</root>')

    for sms in root.findall('.//sms'):
        date = format_unix_timestamp_year_month(int(sms.get('date')))
        address = sms.get('address')
        body = sms.get('body')

        purchase_match = re.search(r'خرید\n(.*?)\n', body)
        if purchase_match:
            purchase = purchase_match.group(1)
        else:
            purchase = "Not Found"

        amount_match = re.search(r'مبلغ:(.*?)\n', body)
        if amount_match:
            amount_str = amount_match.group(1)
            if 'ریال' in amount_str:
                amount_str = amount_str.replace('ریال', '').replace(',', '').strip()
            else:
                amount_str = amount_str.replace(',', '').strip()
            amount = int(amount_str)   # Deduct one zero and convert to integer
        else:
            amount = 0

        sms_data = {
            'date': date,
            'address': address,
            'purchase': purchase,
            'amount': amount
        }

        sms_data_list.append(sms_data)

    return sms_data_list











def create_pdf_table(data):
    doc = SimpleDocTemplate("expenses_summary.pdf", pagesize=letter)
    elements = []

    # Set the font for Persian characters
    pdfmetrics.registerFont(TTFont('Persian', 'Vazir.ttf'))  # Replace with the actual font file path

    # Create a prettier table
    headers = ["Month", "Purchase", "Total Amount"]
    table_data = []
    for month, expenses in data.items():
        sorted_expenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True)
        for purchase, total_amount in sorted_expenses:
            formatted_amount = locale.format_string("%d", total_amount, grouping=True)
            reshaped_purchase = reshape(purchase)
            bidi_purchase = get_display(reshaped_purchase)
            table_data.append([month, bidi_purchase, formatted_amount])

    # Set the font for Persian characters in the table
    table_style = TableStyle([('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONT', (0, 1), (-1, -1), 'Persian'),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table = Table([headers] + table_data, colWidths=[2.5 * inch, 3.5 * inch, 2.5 * inch], repeatRows=1)
    table.setStyle(table_style)

    elements.append(table)
    doc.build(elements)

if __name__ == "__main__":
    xml_file = "sms_data.xml"  # Replace with the actual path to your XML file
    sms_data_list = extract_sms_data(xml_file)

    # Create a defaultdict to group expenses by year and month and purchase
    expenses_by_month = defaultdict(lambda: defaultdict(int))

    for sms_data in sms_data_list:
        date = sms_data['date']
        purchase = sms_data['purchase']
        amount = sms_data['amount']
        
        expenses_by_month[date][purchase] += amount

    # Set locale for formatting amount with commas
    locale.setlocale(locale.LC_ALL, '')  # Use the default locale

    # Create and save the PDF table
    create_pdf_table(expenses_by_month)
    
    print("Results saved to expenses_summary.pdf")

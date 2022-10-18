from flask import Flask, render_template, url_for, Response
from fpdf import FPDF

import psycopg2
import psycopg2.extras

app = Flask(__name__)

# local PostgreSQL database credentials
DB_HOST = "localhost"
DB_NAME = "db2pdf"
DB_USER = "postgres"
DB_PASS = "password"

# connect to test database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Home page view
@app.route('/')
def home():
    return render_template('index.html')

# Report generator page view
@app.route('/download/report/pdf')
def download_report():
    try:
        # create cursor object to navigate through data
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # get person list from table
        cursor.execute("SELECT * FROM staff.person")
        result = cursor.fetchall()

        # create PDF generator onject
        pdf = FPDF()
        # first page!
        pdf.add_page()

        # calculate table width
        table_width = pdf.w - 2 * pdf.l_margin
        # setting font for header
        pdf.set_font('Times', 'B', 14.0)

        # header
        pdf.cell(table_width, 0.0, 'Employee Data', align='C')
        pdf.ln(10)

        # setting font for data rows
        pdf.set_font('Courier', '', 12)

        # need 4 columns with equal width
        col_width = table_width / 4
        pdf.ln(1)
        th = pdf.font_size

        # load data into table rows
        for row in result:
            pdf.cell(col_width, th, str(row['id']), border=1)
            pdf.cell(col_width, th, row['name'], border=1)
            pdf.cell(col_width, th, row['position'], border=1)
            pdf.cell(col_width, th, row['office'], border=1)
            pdf.ln(th)

        pdf.ln(10)

        # footer
        pdf.set_font('Times', '', 10.0)
        pdf.cell(table_width, 0.0, '- end of report -', align='C')

        # and finally let user to download report!
        return Response(
            pdf.output(dest='S').encode('latin-1'),
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment;filename=employee_report.pdf'})
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# application code runner
if __name__ == "__main__":
    app.run()

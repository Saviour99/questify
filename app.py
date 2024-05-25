from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader

app = Flask(__name__)
upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

# Ensure the upload folder exists
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/qna")
def qna():
    return render_template("qna.html")

@app.route('/upload', methods=['POST'])
def uploaded_file():
    file = request.files['file']
    if file.filename != "":
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        reader = PdfReader(open(file_path, "rb"))
        text = ''
        for page_num in range(len(reader.pages)):  #GETTING THE NUMBER OF PAGES
            page = reader.pages[page_num]          #Page Holds the content of each page
            text += page.extract_text()            #Pages are appended in the text variable
        reader.stream.close()                      # Close the PDF file
        return redirect(url_for('upload_mcqs', text=text))
    return "No file uploaded"

@app.route('/upload/mcqs')
def upload_mcqs():
    text = request.args.get('text', '')
    print(text)
    return render_template("mcqs.html", text=text)

if __name__ == "__main__":
    app.run(debug=True)

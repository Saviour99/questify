from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader
from generator import Objective  # The Objective class is in the 'generator' module
import logging

app = Flask(__name__)
app.secret_key = 'Dela'  # Required for session management

upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

# Ensure the upload folder exists
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

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

        content = ""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                content += page.extract_text()

        app.logger.debug("Text Content")

        objective = Objective(content, noOfQues=10)
        mcq_data = objective.generate_test()

        app.logger.debug("MCQ Data Generated: %s", mcq_data)

        # Store the mcq_data in the session
        session['mcq_data'] = mcq_data
        app.logger.debug("Stored MCQ Data in session: %s", session['mcq_data'])

        return redirect(url_for('upload_mcqs'))
    else:
        return "Invalid file type. Please upload a PDF."

@app.route('/upload/mcqs', methods=['GET'])
def upload_mcqs():
    mcqs = session.get('mcq_data', None)  # Retrieve the content from session
    app.logger.debug("Retrieved MCQ Data from session: %s", mcqs)
    return render_template("mcqs.html", mcqs=mcqs)  # Pass content to the template

if __name__ == "__main__":
    app.run(debug=True)

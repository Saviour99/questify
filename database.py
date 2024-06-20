from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from PyPDF2 import PdfReader
from generator import Objective  # The Objective class is in the 'generator' module
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

upload_folder = 'uploads'
app.config['UPLOAD_FOLDER'] = upload_folder

# Ensure the upload folder exists
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Define the model for the MCQ table
class MCQ(db.Model):
    source_file_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False, autoincrement=True)
    question = db.Column(db.String(300), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    file_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False, default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Create the table if it doesn't exist
db.create_all()

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

        app.logger.debug("Text Content: %s", content)

        objective = Objective(content, noOfQues=10)
        mcq_data = objective.generate_test()

        app.logger.debug("MCQ Data Generated: %s", mcq_data)

        # Store mcq_data in the MySQL database
        for mcq in mcq_data:
            new_mcq = MCQ(
                source_file_id=1,  # Example: Replace with actual source_file_id if applicable
                question=mcq['Question'],
                option_a=mcq['Options'][0],
                option_b=mcq['Options'][1],
                option_c=mcq['Options'][2],
                option_d=mcq['Options'][3],
                answer=mcq['Answer'],
                file_name=filename
            )
            db.session.add(new_mcq)
        db.session.commit()

        return redirect(url_for('upload_mcqs'))
    else:
        return "Invalid file type. Please upload a PDF."

@app.route('/upload/mcqs', methods=['GET'])
def upload_mcqs():
    mcqs = MCQ.query.all()
    return render_template("mcqs.html", mcqs=mcqs)

if __name__ == "__main__":
    app.run(debug=True)

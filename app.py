# Install in terminal one by one
# pip install flask
# pip install spacy
# pip install python-pptx
# pip install PyPDF2

from datetime import datetime
from flask import Flask, render_template, request, make_response
import spacy
from collections import Counter
import random
import os
from flask_sqlalchemy import SQLAlchemy
from pptx import Presentation
import PyPDF2
from PyPDF2 import PdfReader  # Import PdfReader


# Retrieve environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance

db = SQLAlchemy(app)
# Define the Q&A model
class QA(db.Model):
    __tablename__ = 'qa_table'
    source_file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(1000), nullable=False)
    option_a = db.Column(db.String(400), nullable=False)
    option_b = db.Column(db.String(400), nullable=False)
    option_c = db.Column(db.String(400), nullable=False)
    option_d = db.Column(db.String(400), nullable=False)
    answer = db.Column(db.String(400), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def generate_mcqs(text, num_questions=5, filename=""):
    # text = clean_text(text)
    if text is None:
        return []

    # Process the text with spaCy
    doc = nlp(text)

    # Extract sentences from the text
    sentences = [sent.text for sent in doc.sents]

    # Ensure that the number of questions does not exceed the number of sentences
    num_questions = min(num_questions, len(sentences))

    # Randomly select sentences to form questions
    selected_sentences = random.sample(sentences, num_questions)

    # Initialize list to store generated MCQs
    mcqs = []

    # Generate MCQs for each selected sentence
    for sentence in selected_sentences:
        # Process the sentence with spaCy
        sent_doc = nlp(sentence)

        # Extract entities (nouns) from the sentence
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        # Ensure there are enough nouns to generate MCQs
        if len(nouns) < 2:
            continue

        # Count the occurrence of each noun
        noun_counts = Counter(nouns)

        # Select the most common noun as the subject of the question
        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]

            # Generate the question stem
            question_stem = sentence.replace(subject, "______")

            # Generate answer choices
            answer_choices = [subject]

            # Add some random words from the text as distractors
            distractors = list(set(nouns) - {subject})

            # Ensure there are at least three distractors
            while len(distractors) < 3:
                distractors.append("[Distractor]")  # Placeholder for missing distractors

            random.shuffle(distractors)
            for distractor in distractors[:3]:
                answer_choices.append(distractor)

            # Shuffle the answer choices
            random.shuffle(answer_choices)

            # Append the generated MCQ to the list
            correct_answer = chr(64 + answer_choices.index(subject) + 1)  # Convert index to letter

            # Add to database
            qa = QA(
                file_name=filename,
                question_id=len(mcqs) + 1,
                question=question_stem,
                option_a=answer_choices[0],
                option_b=answer_choices[1],
                option_c=answer_choices[2],
                option_d=answer_choices[3],
                answer=correct_answer,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            db.session.add(qa)
            db.session.commit()

            mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs


@app.route("/")
@app.route("/home/")
def home():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/admin/")
def admin():
    return render_template("admin.html")

@app.route("/mcqs/")
def mcqs():
    return render_template("qna.html")

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        text = ""

        # Check if files were uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                if file.filename.endswith('.pdf'):
                    # Process PDF file
                    text += extract_pdf(file)
                elif file.filename.endswith('.txt'):
                    # Process text file
                    text += file.read().decode('utf-8')
                elif file.filename.endswith('.pptx'):
                    # Process Powerpoint file
                    text += extract_pptx(file)
            else:
                return "No file selected", 400
        else:
            # Process manual input
            text = request.form['text']

        # Get the selected number of questions from the dropdown menu
        if 'num_questions' in request.form:
            try:
                num_questions = int(request.form['num_questions'])
            except ValueError:
                return "Invalid number of questions", 400
        else:
            return "Number of questions is missing", 400

        mcqs = generate_mcqs(text, num_questions=num_questions, filename=file.filename)  # Pass the selected number of questions
        # Ensure each MCQ is formatted correctly as (question_stem, answer_choices, correct_answer)
        mcqs_with_index = [(i + 1, mcq) for i, mcq in enumerate(mcqs)]
        return render_template('qna.html', mcqs=mcqs_with_index)

    return render_template('upload.html')

def extract_pdf(file):
    # Initialize an empty string to store the extracted text
    text = ""

    # Create a PyPDF2 PdfReader object
    pdf_reader = PdfReader(file)

    # Loop through each page of the PDF
    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page
        page_text = pdf_reader.pages[page_num].extract_text()
        # Append the extracted text to the overall text
        if page_text:
            text += page_text

    return text

def extract_pptx(file):
    # Load the presentation
    presentation = Presentation(file)
    
    # Initialize an empty list to hold all text content
    text= ""
    
    # Iterate through all slides
    for slide in presentation.slides:
        # Iterate through all shapes in the slide
        for shape in slide.shapes:
            # Check if the shape has text
            if hasattr(shape, "text"):
                # Append the text to the string
                text += shape.text
    return text

# Create the database and table(s)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
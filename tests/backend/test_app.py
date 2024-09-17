import pytest

from app import app, db, QA  # Import your Flask app and database

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('test_config.Config')  # Use the test configuration
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create database tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up database after tests

def test_home_page(test_client):
    """Test the home page route"""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Home Page" in response.data

def test_upload_page(test_client):
    """Test the upload page route"""
    response = test_client.get('/upload/')
    assert response.status_code == 200
    assert b"Upload your file" in response.data

def test_file_upload(test_client):
    """Test file upload and MCQ generation"""
    data = {
        'text': 'The cat sat on the mat.',
        'num_questions': '1'
    }
    response = test_client.post('/upload/', data=data)
    assert response.status_code == 200
    assert b"Generated MCQs" in response.data

def test_mcqs_generation(test_client):
    """Test MCQ generation functionality"""
    text = 'The cat sat on the mat. The dog barked loudly.'
    num_questions = 1
    response = test_client.post('/upload/', data={'text': text, 'num_questions': num_questions})
    assert response.status_code == 200
    assert b"Generated MCQs" in response.data
    # Further assertions can be made based on the generated MCQs

def test_pdf_extraction(test_client):
    """Test PDF extraction functionality"""
    # Prepare a PDF file with some text
    with open('test.pdf', 'rb') as f:
        response = test_client.post('/upload/', content_type='multipart/form-data', data={
            'file': (f, 'test.pdf'),
            'num_questions': '1'
        })
    assert response.status_code == 200
    assert b"Generated MCQs" in response.data
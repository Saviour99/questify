# Questify
![Questify](static/images/file7.png)

## Table of Content
- [Introduction](#introduction)
  - [The Project](#the-project)
  - [Inspiration](#inspiration)
  - [The Context](#the-context)
  - [Links](#links)
- [Installation](#installation)
  - [Pre-Installation Process](#pre-installation-process)
  - [Required Software](#required-software)
  - [Installation Process](#installation-process)
    - [Step 1: Clone the Repository](#step-1-clone-the-repository)
    - [Step 2: Change Directory](#step-2-change-directory)
    - [Step 3: Create and Activate a Virtual Environment](#step-3-create-and-activate-a-virtual-environment)
    - [Step 4: Install Dependencies](#step-4-install-dependencies)
- [Usage](#usage)
  - [Upload a File](#upload-a-file)
  - [Select the Number of Questions](#select-the-number-of-questions)
  - [Generate the MCQs](#generate-the-mcqs)
- [Contribution](#contribution)
- [Related Projects](#related-projects)
- [Licensing](#licensing)

## Introduction
 ### The Project
 Questify is a web app that simplifies quiz creation for students and educators by generating multiple-choice questions (MCQs) from uploaded course materials, including PDFs, text files, and slide presentations. It uses text extraction algorithms to analyze the content and generate random MCQs, with each question including four answer options and a correct answer, providing an engaging learning experience.
 <br />
 ### Inspiration
As a student at the Kwame Nkrumah University of Science and Technology (KNUST), specifically during my third and final year at the School of Business, I faced a significant challenge that many students could relate to: the limited access to past exam questions. This limitation left me relying solely on the materials provided by lecturers, which made it difficult to assess my understanding of the topics I studied fully. Without the opportunity to practice with real exam questions, I felt unprepared for the kinds of questions I would face in exams

This experience drove me to take action and create a solution not just for myself, but for other students as well. I developed Questify, a web application designed to bridge this gap by offering students easy access to a platform where they can generate and practice multiple-choice questions. My goal is to provide students at KNUST and beyond with the tools they need to test and strengthen their understanding of the material truly, ultimately making learning more effective and accessible for all.
<br />
 ### The Context
This is my Portfolio Project, concluding my Foundations Year at Holberton School. I chose what I wanted to work on, as long as I presented a working program at the end of the development stage.
<br />
### Links
Visit the **live site**: [Questify Web App](https://questify.saviourdela.tech/)
<br />
Final project **blog**: [Questify - The Journey](#)
<br />
Connect with the author on **LinkedIn**: [Saviour Assandoh](https://www.linkedin.com/in/saviour-assandoh/)
<br />
## Installation

### Pre-Installation Process

Before starting the installation, ensure you have the following installed and configured:

- **Python 3.x** and **pip**
- **MySQL** (or another compatible database)
- **Virtual environment** (recommended)

### Required Software

Questify requires the following dependencies:

- Flask
- Flask-Migrate
- Flask-SQLAlchemy
- spaCy
- Nginx
- Gunicorn
- MySQL-Python Connector
- PyPDF2
- python-pptx

### Installation Process

#### Step 1: Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
$ git clone https://github.com/Saviour99/questify.git
```
#### Step 2: Change Directory

Navigate into the project directory:

```bash
$ cd questify
```

#### Step 3: Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies. Create and activate the virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```
### Step 4: Install Dependencies
Install all the required dependencies listed in the requirements.txt file:

```bash
$ pip install -r requirements.txt
```

## Usage
1. **Upload a File**:
   To begin creating multiple-choice questions (MCQs), click anywhere within the rectangular area marked by a black dashed line. This will open a file explorer window where you can select and upload your study materials. Questify supports files with the following extensions: `.pdf`, `.txt`, and `.pptx`. These formats are commonly used for course materials like textbooks, lecture notes, and slide presentations.
   <br />
   <br />
   ![File Upload](static/images/file2.png)
   <br />
   <br />
   ![File Upload](static/images/file1.png)
   <br />
   <br />

3. **Select the Number of Questions**:
   Once your file is uploaded, you will be prompted to select how many MCQs you would like to generate. The system offers preset options, allowing you to choose between 5, 10, 15, or 20 questions. Simply select the number that fits your quiz or exam requirements. This option helps to customize the length of the quiz based on the depth of content you need.
   <br />
   <br />
   ![Select Number of Questions](static/images/file3.png)
   <br />
   <br />
   ![Select Number of Questions](static/images/file4.png)
   <br />
   <br />

5. **Generate the MCQs**:
   After selecting the desired number of questions, click the **Generate** button. Questify will automatically analyze the content of the uploaded file, extract key information, and generate a set of multiple-choice questions (MCQs) based on the text. Each question will be accompanied by four possible answer choices (A, B, C, and D), with one correct answer identified. This process is quick and ensures that the questions are relevant to the content you've uploaded, saving you time and effort.
   <br />
   <br />
   ![Generate MCQs](static/images/file5.png)
   <br />
   <br />
   ![Generate MCQs](static/images/file6.png)
   <br />
   <br />
## Contribution
Saviour Assandoh is the only contributor at this time

## Related projects
Here is the [repo](https://github.com/Saviour99/) with all my projects.

## Licensing 🔒
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


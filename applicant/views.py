from django.http import HttpResponse
from pathlib import Path
from django.shortcuts import render

from applicant.models import Applicant
from .forms import ApplicantForm
from . import secrets

def home(request):
    context = {
        'form' : ApplicantForm
    }

    if request.method == 'POST':
        applicant_form=ApplicantForm(request.POST, request.FILES)
        if(applicant_form.is_valid()):
            data = applicant_form.save(commit=False)
            file_name = request.FILES['file'].name.replace(' ', '_')
            data.save()

            get_resume_as_dict(f"{Path(__file__).parent.parent}/media/resumes/{file_name}", data.id)
            return render(request, 'applicant/home.html', context)
    
    return render(request, 'applicant/home.html', context)



# Extarct ----------------------------------------
import PyPDF2
import os
import openai
import json

def parsePDF(x):
    fhandle = open(x, 'rb')
    pdfReader = PyPDF2.PdfFileReader(fhandle)
    pagehandle = pdfReader.getPage(0)
    text = pagehandle.extract_text()

    split= text.split("\n")

    for n in split:
        if n == ' ':
            split.remove(n)

    l = [i.strip() for i in split]

    resume = "\n".join(l)

    return resume

def call_OpenAI(x):
    resume = parsePDF(x)

    openai.api_key = secrets.OPEN_AI_KEY

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="A JSON file extracting the most relevant information about the following applicant's work experience:\n\nApplicant 1 Resume:\n\n+1 (984) 837-2465\nDurham, NC\ncs582@duke.edu\nCarlos Gustavo Salas Flores GitHub: cs582\nLinkedIn: carlosgustavosalas\nPortfolio: cs582.github.io/portfolio/\nEDUCATION\nDuke University/Duke Kunshan University, B.S. in Data Science & B.S. in Interdisciplinary Studies Durham, NC + Kunshan, China\nGPA: 3.7/4.0.\nDual-degree, Full Scholarship, and Dean’s list (2019, 2020).\nCoursework: Data Structures and Algorithms, Data Analysis, Data Visualization, Economics, Econometrics, and Machine Learning.\nEXPERIENCE\nAmazon May 2022—Aug 2022\nSoftware Development Engineer Intern Seattle, WA\nDeveloped a web application for AWS Lambda customers that helped to increase availability by 5% (Python).\nHandled 10PB+ of data for customer segmentation and created user profiles (SQL, Numpy and Pandas).\nDesigned a ML pipeline using time-series to identify low availability customers with a 97% accuracy (Scikit-learn).\nBuilt and deployed a data analysis package that saved engineers +100 hours/week (EC2, Docker, S3, and Lambda).\nWorked in a Science Research team and wrote research and technical papers for engineers, scientists, and AWS stakeholders.\nSanford School of Public Policy at Duke University Jan 2022 —May 2022\nData Analysis Research Assistant Durham, NC\nGathered and cleaned US Census and survey data to design social policies that improved accessibility to non-English speakers.\nCompiled more than 15,000,000 data-points in a database (R).\nProduced info-graphics and dashboards to convey information to the general public.\nData Science Research Center at Duke Kunshan University May 2021 —May 2022\nData Science Research Assistant Shanghai, China\nPrepared financial data from the S&P 500 for algorithmic trading (NumPy and Pandas) and achieved 22% return of investment.\nAssessed Reinforcement Learning and Supervised Learning algorithms for time-series forecasting (PyTorch and Scikit-learn).\nEvaluated different approaches to statistical arbitrage trading and optimized pairs trading selection time by more than 50%.\nSKILLS\nProgramming Languages Python, Java, C/C++, R, and SQL\nTechnologies EC2, ECR, Docker, Lambda, S3, Git, and LaTeX\nQuantitative Research ETL, Data Visualization, Clustering, Regression, Statistics, and Time Series\nData Science Libraries NumPy, SciPy, Pandas, Scikit-learn, PyTorch, Matplotlib, Seaborn, and Ggplot\nAnalysis Software QuickSight, Tableau, OpenRefine, and Microsoft Excel\nLanguages English (Fluent), Spanish (Native), and Chinese (Intermediate)\nACHIEVEMENTS\nNational Finalist at the Alibaba GET Challenge (top 12\n\nApplicant 1 JSON:\n\n{\n\"Applicant Information\":\n[\n{\n\"Contact Information\":\n[\n{\"Name\": \"Carlos Gustavo Salas Flores\"},\n{\"School\": \"Duke University/Duke Kunshan University\"},\n{\"Degree\": \"Bachelor of Science in Data Science & Interdisciplinary Studies\"},\n{\"GPA\": \"3.7/4.0\"}\n]\n},\n{\n\"Experience\":\n[\n{\n\"Company 3\":\n[\n{\"Company Name\":\"Amazon (May 2022 - Aug 2022)\"},\n{\"Projects\": [\"Customer Segmentation, Designed ML Pipelines, and Built Analysis Packages\"]},\n{\"Accomplishments\": [\"Increased Availability by 5%, Handled 10PB+ of data, Identified customers with 97% accuracy, and Saved engineers 100+ hours of work\"]}\n]\n},\n{\n\"Company 2\":\n[\n{\"Company Name\":[\"Sanford School of Public Policy at Duke University (Jan 2022 — May 2022)\"]},\n{\"Projects\": [\"Designed social policies\"]},\n{\"Accomplishments\": [\"Compiled more than 15,000,000 data-points and produced infographics and dashboards\"]}\n]\n},\n{\n\"Company 3\":\n[\n{\"Company Name\":\"Data Science Research Center at Duke Kunshan University (May 2021 — May 2022)\"},\n{\"Projects\": [\"Algorithmic Trading\"]},\n{\"Accomplishments\": [\"Achieved 22% return of investment and optimized pairs trading by 50%\"]}\n]\n}\n]\n},\n{\n\"Skills\": [\"Cloud Computing\", \"Machine Learning\", \"Data Science\", \"Data Analysis\", \"Backend Engineering\"]\n},\n{\n\"Technologies\": [\"EC2\", \"ECR\", \"Docker\", \"Lambda\", \"S3\", \"Git\"]\n},\n{\n\"Libraries\": [\"NumPy\", \"SciPy\", \"Pandas\", \"Scikit-learn\", \"PyTorch\", \"Matplotlib\", \"Seaborn\", \"ggplot\"]\n},\n{\n\"Awards\": [\"Alibaba GET National Finalist\", \"IBM AI Engineering Professional Certificate\"]\n}\n]\n}\n\nApplicant 2 Resume:\n\n"+resume+"\n\nApplicant 2 JSON:\n\n{",
        temperature=0,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response

def get_resume_as_dict(x, applicantId):
    string_pseudo_json = call_OpenAI(x)["choices"][0]["text"]
    resume = "{" + string_pseudo_json
    resume = resume.replace("\n", "")
    resume = json.loads(resume)

    Applicant.objects.filter(pk=applicantId).update(processed_resume=resume)

    return resume
# ------------------------------------------------
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
import pymysql
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.metrics import accuracy_score
from application.models import myuser, question, answer
import random
import os
from gtts import gTTS

# from gtts import mygTTS
# import os
# from pydub import AudioSegment
# from pydub.effects import pitch_shift

# def convert_text_to_speech(text):
#     # Generate female voice
#     tts_female = mygTTS(text, lang='en-us')
#     tts_female.save("female_voice.mp3")

#     # Load the generated female voice audio file
#     female_audio = AudioSegment.from_mp3("female_voice.mp3")

#     # Change pitch to make it sound like a male voice
#     pitch_shifted_audio = pitch_shift(female_audio, 3)  # You might need to adjust the value (3 is just an example)

#     # Export the modified audio directly to the existing male voice file
#     pitch_shifted_audio.export("question.mp3", format="mp3")

#     # Play the audio file using the default media player
#     os.system("question.mp3")

#     # Clean up temporary files
#     os.remove("female_voice.mp3")


# Example usage
# text_to_convert = "Hello, this is a sample text."
# convert_text_to_speech(text_to_convert)


def doremove(request):
    if 'email' in request.GET:  # Checking if email parameter exists in the request
        email = request.GET['email']
        # Use Django ORM to delete the user
        myuser.objects.filter(email=email).delete()
        # No need to clear the session variable as you're not using it
        return render(request, "viewuserprofile.html")
    else:
        return redirect('viewuserprofile')


def index(request):
    return render(request,"homepage.html")

def about(request):
    return render(request,"about.html")

def service(request):
    return render(request,"service.html")

def user(request):
     return render(request,"user.html")

def admindashboard(request):
     return render(request,"admindashboard.html")

def questions(request):
     return render(request,"inputquestions.html")

def inputquestions(request):
    inputquestions_text = request.POST.get("inputquestions")  # Renamed variable
    inputanswer = request.POST.get("inputanswer")
    programming_language = request.POST.get("programminglanguage")

    # Mapping of programming languages to uids
    language_to_uid = {
        "python": 1,
        "c": 2,
        "php": 3,
        "HR": 4,
        "frontend": 5,
        "backend": 6,
        "dataanalyst": 7,
        "mernstack": 8,
        "meanstack": 9,
        "ai/ml": 10,
    }
    
    uid = language_to_uid.get(programming_language, None)

    # If the programming language is valid, save the question
    if uid is not None:
        new_question = question(que=inputquestions_text, answer=inputanswer, uid=uid)  # Renamed variable
        new_question.save()

    return render(request, "inputquestions.html")

def showquestion(request):
    # Initialize an empty payload list
    payload = []

    # Fetch all questions from the CQuestion model
    questions = question.objects.all()  # Renamed variable to 'questions'

    # Prepare payload
    for q in questions:  # Changed iteration variable name to 'q'
        content = {
            'que': q.que,  # Changed 'question.question' to 'q.que'
            'answer': q.answer,
            'uid': q.uid
        }
        payload.append(content)

    # Render data to template
    return render(request, "showquestion.html", {'list': {'items': payload}})

    
def dashboard(request):
    return render(request,"admindashboard.html")

    
def login(request):
    return render(request,"loginpanel.html")
    
def logout(request):
    return render(request,"loginpanel.html")

def register(request):
    return render(request,"registrationPanel.html")

def dologin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = myuser.objects.get(email=email, password=password)
    except myuser.DoesNotExist:
        user = None

    if user is not None:
        # Set user information in session
        request.session['id'] = user.id
        request.session['name'] = user.username
        request.session['contact'] = user.contact
        request.session['email'] = user.email
        request.session['password'] = user.password

        return redirect('UserDashboard')  # Redirect to the index page after successful login
    elif email == "admin" and password == "admin":
        return redirect('dashboard') 
    else:
        return render(request, "error.html")



def prevpred(request):
    payload = []
    uid = request.session.get('uid')

    answers = answer.objects.filter(uid=uid)

    # Prepare payload
    for answer in answers:
        content = {'answers': answer.answers}
        payload.append(content)

    return render(request, "prevpred.html", {'list': {'items': payload}})


def doregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')
        myuser.objects.create(username=username, contact=contact, email=email, password=password)
        return render(request, "loginpanel.html")
    else:
        return render(request, "registrationpanel.html") 

def viewpredicadmin(request):
    content={}
    payload=[]
    q1="select * from smp";
    cur=con.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'s1':x[0],"s2":x[1],"s3":x[2],"s4":x[3],'s5':x[4],"s6":x[5],"s7":x[6],"s8":x[7],"pred":x[8],"acc":x[9]}
        payload.append(content)
        content={}
    return render(request,"viewpredadmin.html",{'list': {'items':payload}})


def prevpred(request):
    return render(request,"prevpred.html")

# Define language_to_uid dictionary
language_to_uid = {
        "python": 1,
        "c": 2,
        "php": 3,
        "HR": 4,
        "frontend": 5,
        "backend": 6,
        "dataanalyst": 7,
        "mernstack": 8,
        "meanstack": 9,
        "ai/ml": 10,
    }

# Define myprofile function
def myprofile(request):
    # Initialize an empty payload list
    payload = []

    # Retrieve user ID from session
    id = request.session.get('id')
    user_data = myuser.objects.filter(id=id)

    # If user data exists, prepare payload
    if user_data.exists():
        for data in user_data:
            # Fetch attempted languages from answers
            attempted_languages = answer.objects.filter(userid=data.id).values_list('que', flat=True).distinct()
            
            # Initialize list to store languages and their corresponding uids
            languages = []
            for language in attempted_languages:
                uid = language_to_uid.get(language, None)
                if uid is not None:
                    languages.append({'language': language, 'uid': uid})

            content = {
                'name': data.username,
                'contact': data.contact,
                'email': data.email,
                'languages': languages  # Store languages and their uids in the payload
            }
            payload.append(content)

    return render(request, "myprofile.html", {'list': {'items': payload}})





def viewuser(request):
    # Fetch all UserData objects
    user_data = myuser.objects.all()
    
    # Prepare payload
    payload = []
    for data in user_data:
        content = {
            'name': data.username,
            'contact': data.contact,
            'email': data.email
        }
        payload.append(content)

    # Render data to template
    return render(request, "viewuserprofile.html", {'list': {'items': payload}})

def UserDashboard(request):
        return render(request,"UserDashboard.html")     

def livepred(request):
    return render(request,"predict.html")


def chatbot(request):
    return render(request, 'chatbot.html')

def chat(request):
    return render(request,"chatbot.html")


global count
global lastchat
count = 0

def convert_text_to_speech(text):
    tts = gTTS(text)
    tts.save("static/question.mp3")

import difflib

def calculate_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
    return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def chatbot1(request):
    # Retrieve user session data
    uid = request.session.get('custom_uid', None)
    q6 = request.POST.get('q6')
    userid = request.session.get('id', None)

    # Initialize global count variable if not already initialized
    global count
    if 'count' not in globals():
        count = 0

    # Fetching questions using Django ORM
    questions = question.objects.filter(uid=uid) | question.objects.filter(que=q6)
    questions = [question.que for question in questions]

    context = {'questions': questions, 'uid': uid}

    # Fetching user answer
    user_answer = request.POST.get('answer')

    if questions:
        correct_answer = questions[count].lower() if count < len(questions) else None
    else:
        correct_answer = None

    # Calculate similarity using simple word matching
    similarity = calculate_similarity(user_answer, correct_answer) if user_answer and correct_answer else 0
    current_question = questions[count] if questions and count < len(questions) else None

    print("User Answer:", user_answer)
    print("UID:", uid)
    print("UserID:", userid)
    print("Q6:", q6)

    try:
        # Inserting answer into the Answer table using Django ORM if all necessary data is available
        if user_answer and uid and userid and q6:
            answer.objects.create(answers=user_answer, uid=uid, similarity=similarity, userid=userid, que=q6)
        else:
            print("Answer not saved. Missing data.")

        # Displaying next question or redirecting if count exceeds 10
        if count < 10 and current_question:  # Changed from 15 to 10
            convert_text_to_speech(current_question)  # Convert question to speech
            context['question'] = current_question
            context['is_correct'] = similarity > 0.5
            context['correct_answer'] = correct_answer
            context['similarity'] = similarity
            context['question_number'] = count + 1  # Add question number to context
            context['total_questions'] = 10  # Add total questions to context
            count += 1
            print("Count:", count)
        else:
            print("Test completed. Redirecting to results page.")
            # Reset count for next test
            count = 0
            return question_display(request)

    except Exception as e:
        print("Error:", e)

    return render(request, 'question.html', context)




def c_question_display(request):
    uid = None
    if request.method == 'POST':
        uid = request.POST.get('dropdown')
        print(uid)
        request.session['custom_uid'] = uid
        print(uid)  

    questions = "Tell Me your Name"
    count = 0
    
    context = {'question': questions, 'count': count, 'uid': uid}
    
    # Convert question to speech
    convert_text_to_speech(questions)
    
    return render(request, "question.html", context)



def question_display(request):
    payload = []

    # Retrieve uid from the session
    uid = request.session.get('custom_uid', None)
    
    # Fetching data from the Answer model - limit to last 10 answers
    res = answer.objects.all().order_by('-id')[:10]  # Changed from 15 to 10
    
    print("Question display", res)

    total_score = 0
    for x in res:
        # Convert similarity score to float before rounding
        similarity_score = float(x.similarity)
        # Round similarity score to two decimal places
        similarity_score = round(similarity_score, 2)
        
        # Determine the rating based on similarity score
        if similarity_score >= 0.8:
            rating = "10/10"
            score = 10
        elif similarity_score >= 0.6:
            rating = "8/10"
            score = 8
        elif similarity_score >= 0.4:
            rating = "5/10"
            score = 5
        elif similarity_score >= 0.2:
            rating = "3/10"
            score = 3
        else:
            rating = "0/10"
            score = 0
            
        total_score += score
        
        content = {
            'answers': x.answers, 
            'similarity': similarity_score, 
            'que': x.que,
            'rating': rating
        }
        payload.append(content)

    # Calculate average score
    average_score = round(total_score / len(res) if res else 0, 1)
    
    return render(request, "click.html", {
        'list': {'items': payload},
        'total_questions': 10,
        'average_score': average_score
    })

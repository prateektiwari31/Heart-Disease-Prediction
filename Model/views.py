from django.shortcuts import redirect, render
from .forms import UserRegistrationForm
from django.contrib.auth import login 
import pandas as pd
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

from joblib import load
model=load('./savedModels/model.joblib')

# Create your views here.

def predictor(request):
    return render(request,'main.html')


def formInfo(request):
    # Retrieve and convert query parameters to numeric types
    age = int(request.GET['age'])
    sex = int(request.GET['sex'])
    cp = int(request.GET['cp'])
    trestbps = int(request.GET['trestbps'])
    chol = int(request.GET['chol'])
    fbs = int(request.GET['fbs'])
    restecg = int(request.GET['restecg'])
    thalach = int(request.GET['thalach'])
    exang = int(request.GET['exang'])
    oldpeak = float(request.GET['oldpeak'])
    slope = int(request.GET['slope'])
    ca = int(request.GET['ca'])
    thal = int(request.GET['thal'])

    # Create a DataFrame with feature names
    input_data = pd.DataFrame([{
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal
    }])

    # Predict using the model
    y_pred = model.predict(input_data)

    # Interpret the prediction
    if y_pred[0] == 0:
        y_pred = 'No Heart Disease'
    else:
        y_pred = 'Heart Disease'

    # Render the result page
    return render(request, 'result.html', {'result': y_pred})

def register(request):
    if request.method=='POST':
      form=UserRegistrationForm(request.POST)
      if form.is_valid():
        user=form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request,user)
        return redirect('predictor')
    else:
     form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form' : form})


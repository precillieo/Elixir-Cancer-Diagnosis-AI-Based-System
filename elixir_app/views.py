from django.shortcuts import render,redirect #for rendering htmls
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
# from .models import *
from . import views
# from .forms import *
import os

# from .forms import UploadImage 
from .forms import Image_Upload 
from .forms import SavePatientDetails
from .models import PatientDetails
from .models import Insert
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages




# Create your views here.
# def index(request):
#     return HttpResponse("Hello world. You're at the Elixir_app")
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
def elixir_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('elixir_dashboard')
        else:
            messages.info(request,'Username OR Password is incorrect')


        #  context={'form':form}
    return render(request,'elixir_app/elixir_login.html')

def logoutUser(request):
    logout(request)
    return redirect('elixir_login')

    
def elixir_dashboard(request):
    patient_form = SavePatientDetails()
    if request.method == 'POST':
        patient_form = SavePatientDetails(request.POST)
        if patient_form.is_valid():
            patient_form.save()
        

    context = {'patient_form': patient_form}
    return render(request, 'elixir_app/elixir_dashboard.html', context)
    
    #
""" Model uploading class below"""


BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath(__file__)))

def PredictImage(request):

    # uploadform = UploadImage()
    image_form = Image_Upload()

    context = {'image_form': image_form}

    if request.method == 'POST' and request.FILES['file_name']:

        image_form = Image_Upload(request.POST,request.FILES)

        if image_form.is_valid():

            file_path = request.FILES['file_name']

            image_name = file_path.name

            image_name = str(image_name)

            if image_name.endswith(".jpg") or image_name.endswith(".png"):

                new_file = Insert(filepaths=file_path, filename=image_name)

                new_file.save()
                print("Modeling part now.............")

                # import the necessary packages
                # import keras
                # from keras.preprocessing.image import img_to_array
                # from keras.models import load_model
                # from gpiozero import LEDBoard
                # from gpiozero.tools import random_values
                # from threading import Thread
                # import numpy as np
                # import tensorflow as tf
                import h5py
                # import imutils
                # import time
                # from PIL import Image
                import cv2
                # import os

                # load the image
                print("Loading the image now.............")
                image = cv2.imread(os.path.join(BASE_DIR, 'media/images/' + image_name))
                orig = image.copy()

                # pre-process the image for classification
                print("Preprocessing the image now.............")
                image = cv2.resize(image, (64, 64))
                image = image.astype("float") / 255.0
                image = img_to_array(image)
                image = np.expand_dims(image, axis=0)

                # load the trained convolutional neural network
                print("[INFO] loading model...")
                model = tf.keras.models.load_model(os.path.join(BASE_DIR,'Models/saved_model.h5'))

                # classify the input image
                print("Classifying the image now.............")
                (normal, cancer) = model.predict(image)[0]

                # build the label
                proba = 0
                label = None;

                if normal > cancer:
                    proba = normal
                    label = 'Normal'
                if cancer > normal:
                    proba = cancer
                    label = 'Cancer'
                
                label_string = "{:.2f}%".format(proba*100)

                label = "Uploaded Image Name :  {}, Prediction : {}, Confidence  {:.2f}%".format(image_name,label,proba * 100)

                # draw the label on the image
                output = imutils.resize(orig, width=800,height=400)
                cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,0.7, (0, 255, 0), 2)

                # show the output image
                cv2.imshow("Output Results", output)
                cv2.waitKey(0)

                image_form = Image_Upload()
                img_path = os.path.join(BASE_DIR, 'media/images' + image_name)
                if label == "normal":
                   out_string = "Prediction : " + "COVID and Pneumonia Negative"
                   confidence = "Percentages: " + label_string
                   context = {'uploaded_img_name':orig,'image_form': image_form, 'out_string': out_string,'confidence':confidence}
                   cv2.imshow("Output Results", output)
                   return render(request, 'elixir_app/prediction.html', context=context)
                else:
                   out_string = "Prediction : "+label+' Positive  '
                   confidence = "Confidence: "+label_string
                   context = {'uploaded_img_name':orig,'image_form': image_form, 'out_string': out_string,'confidence':confidence}
                   cv2.imshow("Output Results", output)
                   return render(request, 'elixir_app/prediction.html', context=context)

            else:
                image_form = Image_Upload()

                format_message="Unsupported format, supported format are .png and .jpg "

                return render(request,'elixir_app/prediction.html',{'fmsg':format_message,'image_form':image_form})

        else:
            return render(request,template_name="elixir_app/prediction.html",context=context)

    return render(request,template_name="elixir_app/prediction.html",context=context)

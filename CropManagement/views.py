from django.shortcuts import render
from .forms import UserCreationForm,AddFarm,SoilForm
from django.contrib.auth.views import LoginView,LogoutView
# Create your views here.
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import farm,MyUser,StateWeather,CropWeather,SoilReport
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
#For messages
import json
from django.contrib import messages
#for model
from cities_light.models import City
import pyowm,datetime
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    if request.user.is_authenticated:
        return render(request,'CropManagement/home.html',{'my_template':'CropManagement/base.html'})

    else:
        return render(request, 'CropManagement/index.html',{'my_template':'CropManagement/index.html'})
def signup(request):
    is_register = False;
    form1 = UserCreationForm(request.POST or None)
    if form1.is_valid():
        form_final = form1.save(commit=True)
        is_register = True;
        print(form1.cleaned_data['password1'])
        user = authenticate(email=form1.cleaned_data['email'],
                            password=form1.cleaned_data['password1'],
                            )

        login(request, user)
        return HttpResponseRedirect(reverse('CropManagement:home'))
    else:
        return render(request, 'CropManagement/signup.html', {'form1':form1,'is_register':is_register})



class Login(LoginView):
    template_name = 'CropManagement/login.html'

class Logout(LogoutView):
    next_page = reverse_lazy('CropManagement:home')
    # form_class = < class 'django.contrib.auth.forms.AuthenticationForm'>


class FarmsCreate(LoginRequiredMixin,CreateView,SuccessMessageMixin):
    template_name = 'CropManagement/add_farm.html'
    form_class = AddFarm
    login_url = reverse_lazy('CropManagement:login')
    success_message = "Farm created Succesfully"
    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = MyUser.objects.get(email=self.request.user)
        try:
            self.object.save()
        except:
            return render(self.request,'CropManagement/add_farm.html',{'message':'already exist','form':form})

        return HttpResponseRedirect(self.get_success_url())

@login_required
def FarmList(request):
    farm_list = farm.objects.filter(user=request.user)
    return render(request,'CropManagement/farms.html',{'farm_list':farm_list})


class FarmEdit(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = farm
    form_class = AddFarm

    template_name = 'CropManagement/farm_edit.html'
    success_url = reverse_lazy('CropManagement:farm_list')
    success_message = "Form updated successfully"




class FarmDelete(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    model = farm
    success_url = reverse_lazy('CropManagement:farm_list')
    success_message = "Deleted Succesfully"

class FarmDetail(LoginRequiredMixin,DetailView):
    model = farm
    context_object_name = 'farm_detail'
    template_name = 'CropManagement/farm_details.html'
    temperature = 1
    date = datetime.datetime.today()
    status = "a"
    future_details_weather = []
    future_details_date = []
    future_details_status = []

    def get_weather(self,location):
        owm = pyowm.OWM('bd5e378503939ddaee76f12ad7a97608')
        print(location.name)
        observation = owm.weather_at_place(location.name)
        w = observation.get_weather()
        self.status = w.get_status()
        self.temperature = w.get_temperature(unit='celsius')['temp']

        self.future_details_weather = []
        self.future_details_date = []
        self.future_details_status = []
        fc = owm.daily_forecast(str(location.name))
        f = fc.get_forecast()
        for weather in f:
            self.future_details_weather.append(weather.get_temperature(unit='celsius')['day'])
            self.future_details_date.append(weather.get_reference_time(timeformat='date'))
            self.future_details_status.append(weather.get_status())




    # def getSoilReports(self):



    def get_context_data(self, *args, **kwargs):
        context = super(FarmDetail,self).get_context_data(**kwargs)
        self.get_weather(self.object.location)
        context['temperature'] = self.temperature
        context['status'] = self.status
        context['zipped'] = zip(self.future_details_date,self.future_details_weather,self.future_details_status)
        return context

class CropEdit(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = farm
    fields = ['crop']
    template_name = 'CropManagement/farm_edit.html'
    pk_url_kwarg = 'pk'
    success_message = "Form updated successfully"
    def get_success_url(self):
        return reverse_lazy('CropManagement:farm_detail',args=[self.kwargs['pk']])

@login_required
def OtherFarmer(request,pk):
    data = farm.objects.filter(~Q(user=request.user))
    farm_user = farm.objects.filter(id=pk,user=request.user).first()
    data=data.filter(location__region__exact=farm_user.location.region)
    data_crop_wheat = data.filter(crop__crop_name = 'Wheat').count()
    data_crop_rice = data.filter(crop__crop_name='Rice').count()
    data_crop_sunflower = data.filter(crop__crop_name = 'Sunflower').count()
    data_crop_soyabean = data.filter(crop__crop_name='Soyabean').count()
    data_crop_maize = data.filter(crop__crop_name='Maize').count()
    data_crop_jute = data.filter(crop__crop_name='Jute').count()
    return render(request,'CropManagement/other_farmer.html',{'other_farmer':data,'pk':pk,'data_crop_wheat':data_crop_wheat,
                                                              'data_crop_rice': data_crop_rice,'data_crop_sunflower':data_crop_sunflower,
                                                              'data_crop_soyabean': data_crop_soyabean,
                                                              'data_crop_maize': data_crop_maize,'data_crop_jute':data_crop_jute})

from django.db.models import  Q

def predictCrops(request,pk):
    location = farm.objects.filter(user=request.user,id=pk)[0].location
    print(location.region)

    try:
        state = StateWeather.objects.filter(state=location.region)[0]
        crop = CropWeather.objects.filter(Q(max_temperature__gte = state.avg_temperature)
                                      & Q(min_temperature__lte=state.avg_temperature)
                                      ).all()

    except:
        return HttpResponse("State data is not available <a href='/'>Go back</a>")

    return render(request,'CropManagement/predictCrop.html',{'crop':crop})





#
def predicCropsOnSoil(request,pk):
    try:
        soil_report = SoilReport.objects.first()
        for crop in Crop.objects.all():
            for nut in soil_report:
                if soil_report.organic_carbon < crop.organic_carbon-2:
                    organic_carbon = "Deficient"

                elif crop.organic_carbon - 2 <= soil_report.organic_carbon <= crop.organic_carbon+2:
                    organic_carbon = "Sufficient"

                else:
                    organic_carbon = "Excess"




        return render(request,'CropManagement/soil_predict.html',{})






    except:
        msg  = "First You need to upload soil report"

        return HttpResponse(msg)

from dal import autocomplete


from .models import Crop
class CropAutocomplete(autocomplete.Select2QuerySetView):
     def get_queryset(self):

         qs = Crop.objects.all()


         if self.q:
             qs = qs.filter(crop_name__istartswith=self.q)


         return qs


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs




class AddSoilReport(LoginRequiredMixin,CreateView,SuccessMessageMixin):
    template_name = 'CropManagement/soil_upload.html'
    form_class = SoilForm
    login_url = reverse_lazy('CropManagement:login')

    def get_success_url(self):
        return reverse_lazy('CropManagement:farm_detail',args=[self.kwargs['pk']])

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = MyUser.objects.get(email=self.request.user)

        self.object.farm_name = farm.objects.get(id=self.kwargs['pk'])
        try:
            self.object.save()
        except:
            return render(self.request,'CropManagement/soil_upload.html',{'message':'already exist','form':form})

        return HttpResponseRedirect(self.get_success_url())

import requests
        
def getNews(request):
    news_data = requests.get("https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=latest&apiKey=eb569205b123452cbd7d65832949c229")
    print(news_data)


from .models import MobileRemainder
from .forms import ReminderForm

class CreateReminder(LoginRequiredMixin,CreateView):
    form_class = ReminderForm
    template_name = 'CropManagement/remind.html'
    login_url = reverse_lazy('CropManagement:login')
    # success_message = "Farm created Succesfully"
    def get_success_url(self):
        return HttpResponseRedirect(reverse('CropManagement:farm_detail',args=[self.kwargs['pk']]))
    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.user = MyUser.objects.get(email=self.request.user)
        self.object.farm = farm.objects.get(id=self.kwargs['pk'])
        try:

            form.save()
            print('I am here')
        except :
            return render(self.request, 'CropManagement/remind.html', {'message': 'already exist for this farm', 'form': form})

        return self.get_success_url()
from django_cron import CronJobBase,Schedule
from twilio.rest import Client
def do():
    while(True):
        remind = MobileRemainder.objects.first()
        mobile_number = remind.mobile_no
        mobile_number = '+91' +str( mobile_number)
        water_time = remind.water_remind
        harvest_time = remind.harvest_remind
        water_time = "01:09:55"
        account_sid = 'AC062178d3463fafaf0a8b544ae9601c19'
        auth_token = 'b433c64321419877897401b57a6a5632'
        client = Client(account_sid, auth_token)
        print('frf')
        client.messages.create(from_='+12568278181', to=["+919408595308"], body="Reminder for war=tering")
        if(datetime.datetime.now() is water_time):
            print("Yes")
            client.messages.create(from_='+12568278181', to=[mobile_number], body="Reminder for war=tering")

        if (datetime.datetime.day is harvest_time):
            client.messages.create(from_='+12568278181', to=[mobile_number], body="Reminder for Harvesting")
















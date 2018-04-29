from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import uuid
from django.urls import reverse,reverse_lazy

from cities_light.models import Country,City,Region



class MyUserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')



        user = self.model(

            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password = password,

        )

        user.set_password(password)
        user.save(using=self._db)
        user.is_admin = False
        return user

    def create_superuser(self,first_name,last_name, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(

            email,
            first_name,
            last_name,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=120,blank = False)
    last_name = models.CharField(max_length=120,blank = True)
    is_active = models.BooleanField(default=True)
    is_admin = models   .BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.last_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Crop(models.Model):
    crop_name = models.CharField(max_length=100)

    def __str__(self):
        return self.crop_name


import uuid
class farm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=100)
    farm_area = models.FloatField()
    crop = models.ForeignKey(Crop,on_delete=models.CASCADE,blank=True,null=True)
    location=models.ForeignKey(City,on_delete=models.CASCADE,blank=False)
    def get_absolute_url(self):
        return reverse("CropManagement:farm_detail",kwargs={'pk':self.pk})

    class Meta:
         unique_together=('farm_name','user')



    def __str__(self):
        return self.farm_name



from django.utils import timezone

class SoilReport(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    uploaded_date = models.DateField(default=timezone.datetime.now())
    farm_name=models.ForeignKey(farm,on_delete=models.CASCADE,related_name='that_farm')
    soil_report = models.CharField(max_length=100)
    pH = models.FloatField()
    EC = models.FloatField()
    organic_carbon = models.FloatField(blank=True,default=0)
    available_nitrogen=models.FloatField(blank=True,default=0)
    available_phosphorus= models.FloatField(blank=True,default=0)
    available_potassium =models.FloatField(blank=True,default=0)
    available_zinc=models.FloatField(blank=True,default=0)
    available_boron=models.FloatField(blank=True,default=0)
    available_iron=models.FloatField(blank=True,default=0)
    available_manganese=models.FloatField(blank=True,default=0)
    available_copper=models.FloatField(blank=True,default=0)


    def __str__(self):
        return self.soil_report
    class Meta:
         unique_together=('soil_report','user')



class CropNutrient(models.Model):
    name = models.ForeignKey(Crop,on_delete=models.CASCADE)
    organic_carbon = models.FloatField(blank=True, default=0)
    available_nitrogen = models.FloatField(blank=True, default=0)
    available_phosphorus = models.FloatField(blank=True, default=0)
    available_potassium = models.FloatField(blank=True, default=0)
    available_zinc = models.FloatField(blank=True, default=0)
    available_boron = models.FloatField(blank=True, default=0)
    available_iron = models.FloatField(blank=True, default=0)
    available_manganese = models.FloatField(blank=True, default=0)
    available_copper = models.FloatField(blank=True, default=0)


    def __str__(self):
        return self.name.crop_name

class CropWeather(models.Model):
    name = models.ForeignKey(Crop, on_delete=models.CASCADE)
    min_temperature = models.FloatField(default=0)
    max_temperature = models.FloatField(default=0)
    min_rainfall = models.FloatField(default=0)
    max_rainfall = models.FloatField(default=0)

    def __str__(self):
        return self.name.crop_name


class StateWeather(models.Model):
    state = models.ForeignKey(Region,on_delete=models.CASCADE)
    avg_temperature = models.FloatField(default=0)
    avg_rainfall = models.FloatField(default=0)


    def __str__(self):
        return self.state.name

class MobileRemainder(models.Model):
        user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
        farm = models.ForeignKey(farm,on_delete=models.CASCADE)
        mobile_no = models.PositiveIntegerField()
        water_remind = models.TimeField()
        harvest_remind = models.DateField()
        pesticide_remind =models.TimeField()



from django.conf.urls import url
from .views import signup,Login,home,Logout,FarmsCreate,FarmList,\
                    FarmEdit,FarmDelete,FarmDetail,\
                    CropEdit,OtherFarmer,\
                    predictCrops,CropAutocomplete,LocationAutocomplete,AddSoilReport,predicCropsOnSoil,CreateReminder
app_name = 'CropManagement'
urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^register/$',signup,name='register'),
    url(r'^login/$',Login.as_view(),name='login'),
    url(r'^logout/$',Logout.as_view(),name='logout'),
    url(r'^addFarm/$',FarmsCreate.as_view(),name='add_farm'),
    url(r'^farmlists/$',FarmList,name='farm_list'),
    url(r'^farmedit/(?P<pk>[0-9a-f-]+)$',FarmEdit.as_view(),name='farm_edit'),
    url(r'^farmdelete/(?P<pk>[0-9a-f-]+)$',FarmDelete.as_view(),name='farm_delete'),
    url(r'^farmdetail/(?P<pk>[0-9a-f-]+$)',FarmDetail.as_view(),name='farm_detail'),
    url(r'^cropedit/(?P<pk>[0-9a-f-]+)$',CropEdit.as_view(),name='crop_edit'),
    url(r'^otherfarmers/(?P<pk>[0-9a-f-]+)$',OtherFarmer,name='other_farmer'),
    url(r'^predictcrops/(?P<pk>[0-9a-f-]+)$',predictCrops,name='predictcrops'),
    url(r'^cropsearch/$',CropAutocomplete.as_view(),name='crop_autocomplete'),
    url(r'^location/$',LocationAutocomplete.as_view(),name='location'),
    url(r'^soilreport/(?P<pk>[0-9a-f-]+)$',AddSoilReport.as_view(),name='soil_upload'),
    url(r'^predictsoil/(?P<pk>[0-9a-f-]+)$',predicCropsOnSoil,name='soil_predict'),
    url(r'^createreminder/(?P<pk>[0-9a-f-]+)$',CreateReminder.as_view(),name='create_reminder'),
    # url(r'^sendremainder/$',send_remainder),


]
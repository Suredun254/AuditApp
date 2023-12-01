from django.urls import path,re_path
from . import views
from django.contrib.auth import views as auth_views

#define app name
app_name='audits'

#create url patterns
urlpatterns = [
    path('',views.dashboard, name='home'),
    path('audit/',views.audit,name='audit'),
    path('facilities/',views.facilities,name='facilities'),
    path('history',views.history,name='history'),
    path('stats/<id>/',views.energyStats,name='stats'),
    path('add/equipment/<id>/',views.addEquipment,name='addEquipment'),
    path('doAudit/',views.do_audit,name='doaudit'),
    path('facilityAudit/<id>/',views.facility_audit,name='facilityAudit'),
    path('facilityStats/<id>/',views.energyStats,name='facilityStats'),
    
    path('auditAnalysis/<id>/',views.auditAnalysis,name='auditanalysis'),
    path('deletefacility/<id>/',views.delete_facility,name='deletefacility'),
    path('deleteequipment/<id>/',views.delete_equipment,name='deleteequipment'),
    path('guest/',views.guestDashboard,name='guest'),
    
]
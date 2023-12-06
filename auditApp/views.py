from django.shortcuts import render,redirect
from datetime import date
from .models import EnergyAudit,EnergyDevice,Facility

from openai import OpenAI
from openai import api_key
from django.http import HttpResponseRedirect
import requests
import ast
# Create your views here.
def dashboard(request):
    
    message=''
    today=date.today()
    
    audits=EnergyAudit.objects.filter(user=request.user)
    facilities=Facility.objects.filter(user=request.user)
    
    audits_count=audits.count()
    facility_count=facilities.count()
    
    highest_audit=0
    facility=''
    
    
    for audit in audits:
        if audit.audit_result > highest_audit:
            highest_audit=audit.audit_result 
            facility=audit.facility.name
            
    try:
        latest_audit=audits.last()
        
    except:
        latest_audit=None
        
    if latest_audit:
        latest_facility=latest_audit.facility
        
        devices=EnergyDevice.objects.filter(facility=latest_facility)
    else :
        devices=None    
        
    
    context={
        "devices":devices,
        'latest_audit':latest_audit,
        'date':today,
        'message':message,
        'audits':audits,
        'audits_count':audits_count,
        'facility_count':facility_count,
        'highest_audit':highest_audit,
        'facility':facility, 
    }
    
    return render(request,'auditApp/dashboard.html',context)

def facilities(request):
    message=""
    
    if request.method=='POST':
        name=request.POST['facility']
        location=request.POST['location']
        
        facility=Facility.objects.create(name=name, location=location,user=request.user)
        facility.save()
        message="Faclity registered"
        
    today=date.today()
    facilities=Facility.objects.filter(user=request.user)
    
    
    context={
        'date':today,
        'facilities':facilities,
        'message':message,
    }
    
    return render(request,'auditApp/facilities.html',context)


def audit(request):
    message=''
    today=date.today()
    
    audits=EnergyAudit.objects.filter(user=request.user)
    
    
    
    context={
        'date':today,
        'message':message,
        'audits':audits,
        
    }
    
    return render(request,'auditApp/audit.html',context)

def addEquipment(request,id):
    message=""
    
    today=date.today()
    
    if request.method=='POST':
        
        device=request.POST['device']
        rating=request.POST['rating']
        facility=Facility.objects.get(pk=id)
        new_device=EnergyDevice.objects.create(name=device,facility=facility,rating=rating,user=request.user)
        new_device.save()
        message="Equipment Added"
        
    devices=EnergyDevice.objects.filter(facility=id,user=request.user)
    print(devices)
    
    context={
        'date':today,
        'devices':devices,
        'message':message,
        "id":id
    }
    
    
    return render(request,'auditApp/addequipment.html',context)

def energyStats(request,id):
    message=''
    today=date.today()
    facility=Facility.objects.get(pk=id)
    
    audits=EnergyAudit.objects.filter(user=request.user,facility=facility)
    
    try:
        latest_audits=audits.order_by('-id')[:3]
    except:
        latest_audits=audits
    
    
    
    context={
        'latest_audits':latest_audits,
        'date':today,
        'message':message,
        'audits':audits,
        'facility':facility.name,
        
    }
    
    return render(request,'auditApp/energystats.html',context)


def history(request):
    
    return render(request,'auditApp/history.html')

def do_audit(request):
    message=""
        
    today=date.today()
    facilities=Facility.objects.filter(user=request.user)
    
    context={
        'date':today,
        'facilities':facilities,
        'message':message,
    }
    
    return render(request,'auditApp/doaudit.html',context)

def facility_audit(request,id):
    message='message'
    today= date.today()
    facility=Facility.objects.get(pk=id)
    devices=EnergyDevice.objects.filter(facility=facility,user=request.user)
    my_devices=[]
    
    for device in devices:
        my_devices.append(device.name)
    prompt=f'i have the following devices {my_devices} in my {facility.name}. How can i save power'
    
    
    
    
    if request.method=='POST':
        
        audit_result=0
        operation_hours=[]
        device_list=[]
        
        for device in devices:
            device_list.append(device.name)
            operation=request.POST[f'operation{device.id}']
            number=request.POST[f'operation{device.id}']
                        
            operation_hours.append(operation)
            rating=EnergyDevice.objects.get(pk=device.id).rating
           
            equipmentUsage=float(operation)*rating *float(number)
            audit_result += equipmentUsage

        audit_result=audit_result/1000
        
        meter_reading=request.POST['meter']
        # no_of_users=request.POST['users']
        # per_capita_consumption=audit_result/no_of_users  
        
        audit_instance = EnergyAudit.objects.create(
            user = request.user,
            facility = facility,
            
            operation_hours = str(operation_hours),
            audit_result = audit_result,
            meter_reading=meter_reading,
            
                
        )
        devices=EnergyDevice.objects.filter(facility=facility,user=request.user)
        
        audit_instance.devices.set(devices)
        
        try:
            prediction=generate_chat_prediction(prompt)
            audit_instance.recommendation=prediction
        except:
            pass
        
        audit_instance.save()
        
        return redirect('audits:audit')
        
            
    
    context={
        "id":id,
        "date":today,
        "message":message,
        'devices': devices
        
    }
    
    return render(request,'auditApp/facilityaudit.html',context)



# Set your OpenAI API key

def generate_chat_prediction(prompt):
    
    client = OpenAI(
        #set your key here
        api_key='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',
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled energy audit operator with knowledge in Energy conservation and management"},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message

def guestDashboard(request):
    
    message=''
    today=date.today()
    
    if request.method=='POST':
        
        prompt=request.POST['guest-prompt']
        my_prompt=f''
        recommendation=generate_chat_prediction(my_prompt)
    
    context={
        'date':today,
        'message':message, 
        "request":request,
        
    }
    
    return render(request,'auditApp/guestdashboard.html',context)
    
    
def auditAnalysis(request,id):
    message=''
    today=date.today()
    auditobject=EnergyAudit.objects.get(pk=id)
    facility=auditobject.facility
    devices=EnergyDevice.objects.filter(facility=facility)
    
    #for device in devices:
    
    recommendation=auditobject.recommendation
    operation_hrs=auditobject.operation_hours

    try:
        list_of_numbers = ast.literal_eval(operation_hrs)
    except(SyntaxError, ValueError):
        print("Error: Unable to convert the string to a list of numbers")
        list_of_numbers=[]
    
    values=[]
    for device,hour in zip(devices,list_of_numbers):
        values.append(float(device.rating)* float(hour))
    
    context={
        'date':today,
        'values':values,
        'message':message, 
        "request":request,
        "devices":devices,
        " recommendation": recommendation,
        
    }
    
    return render(request,'auditApp/auditAnalysis.html',context)

def delete_facility(request,id):

    facility=Facility.objects.get(pk=id)
    facility.delete()

    return redirect('audits:facilities')

def delete_equipment(request,id):
    devices=EnergyDevice.objects.all()
    print(id,'iiiii')
    for device in devices:
        print(device.id,'uuu')

    equipment=EnergyDevice.objects.get(pk=id)
    equipment.delete()

    return redirect('audits:facilities')

    

        
        







from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import date

# Create your views here.

def userhome(request):
    return render(request, 'userhome.html')
def admin(request):
    # show a compact doctors list on admin dashboard
    doctors = Doctor.objects.all()[:10]
    approved_count = Doctor.objects.filter(loginid__login_status=1).count()
    pending_count = Doctor.objects.filter(loginid__login_status=0).count()
    rejected_count = Doctor.objects.filter(loginid__login_status=2).count()
    return render(request, 'admin.html', {
        'doctors': doctors,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
    })

def adminheader(request):
    return render(request, 'adminheader.html')

def landing(request):
    return render(request, 'landing.html')

def userregister(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        user_form = UserForm(request.POST)
        if login_form.is_valid() and user_form.is_valid():
            login_instance = login_form.save(commit=False)
            login_instance.user_type = 'user'
            login_instance.save()
            user_instance = user_form.save(commit=False)
            user_instance.loginid = login_instance
            user_instance.save()
            # return HttpResponse("User registered successfully.")
    else:
        login_form = LoginForm()
        user_form = UserForm()
    return render(request, 'user_register.html', {'login_form': login_form, 'user_form': user_form})
# from .forms import LoginForm, DoctorForm

def doctorregister(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if login_form.is_valid() and doctor_form.is_valid():
            login_instance = login_form.save(commit=False)
            login_instance.user_type = 'doctor'
            login_instance.save()
            doctor_instance = doctor_form.save(commit=False)
            doctor_instance.loginid = login_instance
            doctor_instance.save()
            return redirect("landing")
    else:
        login_form = LoginForm()
        doctor_form = DoctorForm()
    return render(request,'doctorregisteration.html', {'login_form': login_form, 'doctor_form': doctor_form}
    )

def doctorhome(request):
    return render(request, 'doctorhome.html')

def userheader(request):
    return render(request, 'userheader.html')

def doctorheader(request):
    return render(request, 'doctorheader.html')

def userhospitalsearch(request):
    query = request.GET.get('q') 
    if query:
        doctors = Doctor.objects.filter(
            Q(hospital_name__icontains=query) |
            Q(district__icontains=query) |
            Q(city__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()
    return render(request, 'userdoctorview.html', {'doctors': doctors, 'query': query})

def loginform(request):
    if request.method=='POST':
       form=CustomloginForm(request.POST)
       print(form)
       if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            if email == 'admin@gmail.com' and password == 'admin123':
               return redirect('admin')
            # elif email == 'admin@gmail.com' and password == 'admin123':
            #    return redirect('admin_header')
            try:
                user=Login.objects.get(email=email)
                if user.password==password and user.user_type=='user':
                    request.session['user_id']=user.id
                    return redirect('userhome')
                elif user.password==password and user.user_type=='doctor'and user.login_status==1:
                    request.session['doctor_id']=user.id
                    return redirect('doctorhome')
                elif user.password==password and user.user_type=='hospital'and user.login_status==1:
                    request.session['hospital_id']=user.id
                    return redirect('hospitalhome')
                elif user.password==password and user.user_type=='ambulance'and user.login_status==1:
                    request.session['ambulance_id']=user.id
                    return redirect('ambulancehome')
                else:
                    messages.error(request,'Invalid email or password')
            except Login.DoesNotExist:
                messages.error(request,'user does not exist')
    else:
        form=CustomloginForm()
    return render(request,'login.html',{'form':form})

def appointment(request, id):
    user_id = request.session.get('user_id')
    data = User.objects.get(loginid=user_id)
    doctor_data = Doctor.objects.get(id=id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, initial={'doctor': doctor_data})
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user_id = data
            appointment.doctor_id = doctor_data
            appointment.consultationfee = doctor_data.consultationfee 
            appointment.save()
            return redirect('payment', id=appointment.id)
    else:
        form = AppointmentForm(initial={'doctor': doctor_data})

    return render(request, 'appointment.html', {
        'form': form,
        'doctor': doctor_data
    })


def payment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.Appointmentid  = appointment
            payment.amount_paid = appointment.consultationfee
            payment.save()
            appointment.Payment_status = 1
            appointment.save()
            return redirect('userhospitalsearch')
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {
        'form': form,
        'appointment': appointment
    })


def appointmentlist(request):
    a=request.session.get('doctor_id')
    if not a:
      return redirect('landing')
    doc_id = request.session.get('doctor_id')
    doctor = get_object_or_404(Doctor, loginid=doc_id)
    appointments = Appointment.objects.filter(doctor_id=doctor)

    return render(request, 'doctor_appointmentview.html', {
        'appointments': appointments,
        # 'selected_hospital': doctor.hospital_name 
    })

def prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointmentlist')
    else:
        form = PrescriptionForm(instance=appointment)
    return render(request, 'prescription.html', {'form': form, 'appointment': appointment})

def userappointmetview(request):
    a=request.session.get('user_id')
    if not a:
        return redirect('landing')
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)
    appointments = Appointment.objects.filter(user_id=user)
    return render(request, 'userappointmetview.html', {'appointments': appointments})

def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('userappointmetview')

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('userappointmetview')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})

def doctorprofile(request):
     id= request.session.get('doctor_id')
     if not id:
         return redirect('login')
     data =Doctor.objects.get(loginid=id)
     lo_data=Login.objects.get(id=id)
     if request.method ==  'POST':
        form = DoctorForm(request.POST,instance=data)
        form1 = UpdateLoginForm(request.POST,instance=lo_data)
        if form.is_valid() and form1.is_valid():
            login_id = form1.save()
            login_id.save()
            a = form.save(commit=False)
            a.save()  
        return redirect('doctorhome')
     else:
        form =DoctorForm(instance=data)
        form1 = UpdateLoginForm(instance=lo_data)
        return render(request, 'doctorprofile.html',{'form': form,'form1': form1})

def userprofile(request):
     id= request.session.get('user_id')
     if not id:
         return redirect('login')
     data = User.objects.get(loginid=id)
     lo_data=Login.objects.get(id=id)
     if request.method ==  'POST':
        form = UserForm(request.POST,instance=data)
        form1 = UpdateLoginForm(request.POST,instance=lo_data)

        if form.is_valid() and form1.is_valid():
            login_id = form1.save()
            login_id.save()
            a = form.save(commit=False)
            a.save()  
        return redirect('userhome')
     else:
        form =UserForm(instance=data)
        form1 = UpdateLoginForm(instance=lo_data)
        return render(request, 'Userprofile.html',{'form': form,'form1': form1,'id': data.id})
     

def prescriptionview(request):
    doc_id = request.session.get('doctor_id')
    doctor = get_object_or_404(Doctor, loginid=doc_id)
    appointments = Appointment.objects.filter(doctor_id=doctor)

    return render(request, 'prescriptionview.html', {'appointments': appointments})
     
def prescriptionedit(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('prescriptionview')
    else:
        form = PrescriptionForm(instance=appointment)
    return render(request, 'prescriptionedit.html', {'form': form, 'appointment': appointment})



def prescriptiondelete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect('prescriptionview')

def admindoctorview(request):
    doctors = Doctor.objects.all()
    return render(request, 'admindoctorview.html', {'doctors': doctors})

def admindoctorapprove(request, id):
    doctor = get_object_or_404(Doctor, loginid__id=id)
    doctor.loginid.login_status = 1   # integer, not string
    doctor.loginid.save()
    return redirect('admindoctorview')

def admindoctorreject(request, id):
    doctor = get_object_or_404(Doctor, loginid__id=id)
    doctor.loginid.login_status = 2
    doctor.loginid.save()
    return redirect('admindoctorview')

def complaint(request):
    a=request.session.get('user_id')
    if not a:
        return redirect('landing')
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint_instance = form.save(commit=False)
            complaint_instance.user_id = user
            complaint_instance.save()
            return redirect('userhome')
    else:
        form = ComplaintForm()
    return render(request, 'complaint.html', {'form': form})

def complaintview(request):
    a=request.session.get('user_id')
    if not a:
        return redirect('landing')
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)
    complaints = Complaint.objects.filter(user_id=user)
    return render(request, 'complaintview.html', {'complaints': complaints})

def complaintedit(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('complaintview')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'complaintedit.html', {'form': form, 'complaint': complaint})

def complaintdelete(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    return redirect('complaintview')

def complaintreply(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        form = ComplaintReplyForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('admincomplaintview')
    else:
        form = ComplaintReplyForm(instance=complaint)
    return render(request, 'complaintreply.html', {'form': form, 'complaint': complaint})

def admincomplaintview(request):
    complaints = Complaint.objects.all()
    return render(request, 'admincomplaintview.html', {'complaints': complaints})

def logout(request):
    request.session.flush()
    return redirect('landing')

def feedback(request,id):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)
    appointment = get_object_or_404(Appointment, id=id)
    doctor = appointment.doctor_id
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_instance = form.save(commit=False)
            feedback_instance.user_id = user
            feedback_instance.doctor_id = doctor
            feedback_instance.save()
            return redirect('userhome')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def feedbackview(request):
    a=request.session.get('user_id')
    if not a:
        return redirect('landing')
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)
    feedbacks = Feedback.objects.all()  # everyone can view
    return render(request, 'feedbackview.html', {
        'feedbacks': feedbacks,
        'current_user': user
    })

def feedbackedit(request,id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedbackview')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedbackedit.html', {'form': form, 'feedback': feedback})

def feedbackdelete(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    feedback.delete()
    return redirect('feedbackview')

def landingheader(request):
    return render(request, 'landingheader.html')


# def videoconference(request):
#     return render(request, 'videoconference.html')

from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
def videoconference(request, id):
    tjob = get_object_or_404(Appointment, id=id)
    return render(request, 'videoconference.html', {'tjob': tjob})
@csrf_exempt
def save_video_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tempjob_id = data.get("tempjob_id")
        url = data.get("url")
        try:
            tjob = Appointment.objects.get(id=tempjob_id)
            tjob.url = url
            tjob.save()
            return JsonResponse({"status": "success", "url": url})
        except Appointment.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Appointment not found"}, status=404)
    return JsonResponse({"status": "fail"}, status=400)

def hospitalhome(request):
    login_id = request.session.get("hospital_id")
    if not login_id:
        return redirect('login')
    hospital = get_object_or_404(Hospitalreg, loginid=login_id)
    return render(request, "hospitalhome.html", {"hospital": hospital})

def hospitalheader(request):
    return render(request, 'hospitalheader.html')

def hospitalregister(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        hospital_form = HospitalForm(request.POST)
        if login_form.is_valid() and hospital_form.is_valid():
            login_instance = login_form.save(commit=False)
            login_instance.user_type = 'hospital'
            login_instance.save()
            hospital_instance = hospital_form.save(commit=False)
            hospital_instance.loginid = login_instance
            hospital_instance.save()
            return redirect("landing")
    else:
        login_form = LoginForm()
        hospital_form = HospitalForm()
    return render(request,'hosipitalregisteration.html', {'login_form': login_form, 'hospital_form': hospital_form}
    )  

def hospitalprofile(request):
     id= request.session.get('hospital_id')
     if not id:
         return redirect('login')
     data =Hospitalreg.objects.get(loginid=id)
     lo_data=Login.objects.get(id=id)
     if request.method ==  'POST':
        form = HospitalForm(request.POST,instance=data)
        form1 = UpdateLoginForm(request.POST,instance=lo_data)
        if form.is_valid() and form1.is_valid():
            login_id = form1.save()
            login_id.save()
            a = form.save(commit=False)
            a.save() 
        return redirect('hospitalhome')
     else:
        form =HospitalForm(instance=data)
        form1 = UpdateLoginForm(instance=lo_data)
        return render(request, 'hospitalprofile.html',{'form': form,'form1': form1}) 
     
def ambulanceregistration(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        ambulance_form = AmbulanceForm(request.POST)
        if login_form.is_valid() and ambulance_form.is_valid():
            login_instance = login_form.save(commit=False)
            login_instance.user_type = 'ambulance'
            login_instance.save()
            ambulance_instance = ambulance_form.save(commit=False)
            ambulance_instance.loginid = login_instance
            ambulance_instance.save()
            return redirect("landing")
    else:
        login_form = LoginForm()
        ambulance_form = AmbulanceForm()
    return render(request,'ambulanceregistration.html', {'login_form': login_form, 'ambulance_form': ambulance_form}
    )

def ambulancehome(request):
    return render(request, 'ambulancehome.html')    

def ambulanceheader(request):
    return render(request, 'ambulanceheader.html')  

def ambulancelistview(request):
    a=request.session.get('hospital_id')
    if not a:
        return redirect('landing')
    id= request.session.get('hospital_id')
    hospital = get_object_or_404(Hospitalreg, loginid=id)
    ambulances = Ambulance.objects.filter(hospital=hospital)
    return render(request, 'ambulancelistview.html', {'ambulances': ambulances})

def ambulanceapprove(request, id):
    ambulance = get_object_or_404(Ambulance, loginid__id=id)
    ambulance.loginid.login_status = 1   # integer, not string
    ambulance.loginid.save()
    return redirect('ambulancelistview')

def ambulancereject(request, id):
    ambulance = get_object_or_404(Ambulance, loginid__id=id)
    ambulance.loginid.login_status = 2
    ambulance.loginid.save()
    return redirect('ambulancelistview')

def ambulanceprofile(request):
        id= request.session.get('ambulance_id')
        if not id:
            return redirect('login')
        data =Ambulance.objects.get(loginid=id)
        lo_data=Login.objects.get(id=id)
        if request.method ==  'POST':
            form = AmbulanceForm(request.POST,instance=data)
            form1 = UpdateLoginForm(request.POST,instance=lo_data)
            if form.is_valid() and form1.is_valid():
                login_id = form1.save()
                login_id.save()
                a = form.save(commit=False)
                a.save() 
            return redirect('ambulancehome')
        else:
            form =AmbulanceForm(instance=data)
            form1 = UpdateLoginForm(instance=lo_data)
        
            return render(request, 'ambulanceprofile.html',{'form': form,'form1': form1})

def transferpatient(request,id):
    query = request.GET.get('q') 
    if query:
        hospitals = User.objects.filter(
            Q(name__icontains=query) |
            Q(contact__icontains=query) 
        )
    else:
        hospitals = User.objects.all()
    return render(request, 'transferpatient.html', {'hospitals': hospitals, 'query': query})

def assignpatient(request, id):
    # user = get_object_or_404(User, id=id)
    user = get_object_or_404(User, id=id)
    # Determine current actor: ambulance or hospital
    ambulance = None
    hospital = None
    ambulance_id = request.session.get('ambulance_id')
    hospital_id = request.session.get('hospital_id')
    if ambulance_id:
        ambulance = get_object_or_404(Ambulance, loginid=ambulance_id)
    if hospital_id:
        hospital = get_object_or_404(Hospitalreg, loginid=hospital_id)
    # If neither ambulance nor hospital is logged in, require login
    if not ambulance and not hospital:
        return redirect('login')
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            assign_instance = form.save(commit=False)
            # If ambulance is logged in, use it; otherwise expect ambulance_select from hospital
            if ambulance:
                assign_instance.Ambulance_loginid = ambulance
                ambulance.availability=1
                ambulance.save()
            else:
                sel_amb_id = request.POST.get('ambulance_select')
                if sel_amb_id:
                    # Try several lookup strategies but do not raise a 404 to the user
                    selected_amb = None
                    try:
                        selected_amb = Ambulance.objects.get(id=int(sel_amb_id))
                    except (ValueError, Ambulance.DoesNotExist):
                        try:
                            # maybe the posted value was the Login id
                            selected_amb = Ambulance.objects.get(loginid__id=sel_amb_id)
                        except Ambulance.DoesNotExist:
                            selected_amb = None
                    if not selected_amb:
                        messages.error(request, 'Selected ambulance not found. Please choose a valid ambulance.')
                        ambulances = Ambulance.objects.filter(hospital=hospital) if hospital else None
                        return render(request, 'assignpatient.html', {
                            'form': form,
                            'ambulances': ambulances,
                            'ambulance': ambulance
                        })
                    assign_instance.Ambulance_loginid = selected_amb
                else:
                    messages.error(request, 'Please select an ambulance to assign.')
                    ambulances = Ambulance.objects.filter(hospital=hospital) if hospital else None
                    return render(request, 'assignpatient.html', {
                        'form': form,
                        'ambulances': ambulances,
                        'ambulance': ambulance
                    })
            assign_instance.user_loginid = user
            assign_instance.h_loginid = hospital
            assign_instance.save()
            return redirect('ambulancelistview')
    else:
        form = AssignForm()
    ambulances = None
    if hospital and not ambulance:
        ambulances = Ambulance.objects.filter(hospital=hospital)
    return render(request, 'assignpatient.html', {
        'form': form,
        'ambulance': ambulance,
        'ambulances': ambulances,
    })

def ambulanceassignlistview(request):
    a=request.session.get('ambulance_id')
    if not a:
        return redirect('landing')
    ambulance_id = request.session.get('ambulance_id')
    ambulanceloginid = get_object_or_404(Ambulance, loginid=ambulance_id)
    assign = Assign.objects.filter(Ambulance_loginid=ambulanceloginid)
    return render(request, 'ambulance_assignlist_view.html', {'assign': assign})

def confirmation(request, id):
    assign = get_object_or_404(Assign, id=id)
    assign.status = 1
    assign.save()
    assign.Ambulance_loginid.availability = 0
    assign.Ambulance_loginid.save()
    return redirect('ambulanceassignlistview')

def ambulance_confirm_list(request):
    a=request.session.get('hospital_id')
    if not a:
        return redirect('landing')
    id = request.session.get('hospital_id')
    hospital = get_object_or_404(Hospitalreg, loginid=id)
    ambulances = Ambulance.objects.filter(hospital=hospital)
    confirmed_assignments = Assign.objects.select_related(
        'Ambulance_loginid'
    ).filter(
        Ambulance_loginid__in=ambulances,
        status=1
    )
    return render(
        request,
        'ambulance_confirm list.html',
        {'confirmed_assignments': confirmed_assignments}
    )


# def chat(request,reciever_id):
#     user_id = request.session.get('user_id')
#     user = get_object_or_404(User, loginid=user_id)

#     if request.method == 'POST':
#         form = ChatForm(request.POST)
#         if form.is_valid():
#             chat_instance = form.save(commit=False)
#             chat_instance.sender = user.loginid
#             # For simplicity, let's assume the receiver is a fixed user (e.g., admin)
#             receiver = get_object_or_404(Login, id=1)  # Replace with actual receiver logic
#             chat_instance.receiver = receiver
#             chat_instance.save()
#             return redirect('userhospitalsearch')
#     else:
#         form = ChatForm()

#     chats = Chat.objects.all().order_by('timestamp')

#     return render(request, 'chat.html', {
#         'form': form,
#         'chats': chats
#     })

def chat(request, receiver_id):
    user_id = request.session.get('user_id')
    doctor_id = request.session.get('doctor_id')
    hospital_id = request.session.get('hospital_id')
    ambulance_id = request.session.get('ambulance_id')
    sender = None
    if user_id:
        sender = get_object_or_404(Login, id=user_id)
    elif doctor_id:
        sender = get_object_or_404(Login, id=doctor_id)
    elif hospital_id:
        sender = get_object_or_404(Login, id=hospital_id)
    elif ambulance_id:
        sender = get_object_or_404(Login, id=ambulance_id)
    else:
        return redirect('login')
    receiver = get_object_or_404(Login, id=receiver_id)
    # Receiver name (cover User, Doctor, Hospitalreg, Ambulance)
    if User.objects.filter(loginid=receiver).exists():
        receiver_name = User.objects.get(loginid=receiver).name
    elif Doctor.objects.filter(loginid=receiver).exists():
        receiver_name = Doctor.objects.get(loginid=receiver).name
    elif Hospitalreg.objects.filter(loginid=receiver).exists():
        receiver_name = Hospitalreg.objects.get(loginid=receiver).hospital_name
    elif Ambulance.objects.filter(loginid=receiver).exists():
        receiver_name = Ambulance.objects.get(loginid=receiver).driver_name
    else:
        receiver_name = "User"
    messages = Chat.objects.filter(
        Q(sender=sender, receiver=receiver) |
        Q(sender=receiver, receiver=sender)
    ).order_by('timestamp')
    # Mark received messages as read
    Chat.objects.filter(
        sender=receiver,
        receiver=sender,
        is_read=False
    ).update(is_read=True)
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            Chat.objects.create(
                sender=sender,
                receiver=receiver,
                chat=message
            )
            return redirect("chat", receiver_id=receiver_id)
    return render(request, "chat.html", {
        "messages": messages,
        "sender": sender,
        "receiver": receiver,
        "receiver_name": receiver_name
    })

def chatview(request):
    doc_id = request.session.get('doctor_id')
    doctor = get_object_or_404(Doctor, loginid=doc_id)
    chats = Chat.objects.filter(
        Q(sender__id=doctor.id) |
        Q(receiver__id=doctor.id)
    ).order_by('timestamp')
    return render(request, 'chatview.html', {'chats': chats})

def chatreply(request, id):
    chat = get_object_or_404(Chat, id=id)
    if request.method == 'POST':
        form = chatreplyForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            return redirect('chatview')
    else:
        form = chatreplyForm(instance=chat)
    return render(request, 'chatrply.html', {'form': form, 'chat': chat})

def userchatview(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)
    chats = Chat.objects.filter(
        Q(sender__id=user.loginid.id) | Q(receiver__id=user.loginid.id)
    ).order_by('timestamp')
    return render(request, 'userchatview.html', {'chats': chats})

def test(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    user = appointment.user_id
    doctor = appointment.doctor_id
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test_instance = form.save(commit=False)
            test_instance.user_id = user
            test_instance.doctor_id = doctor
            test_instance.Appointmentid = appointment
            test_instance.save()
            return redirect('appointmentlist')
    else:
        form = TestForm()
    return render(request, 'test.html', {'form': form, 'appointment': appointment})

def testedit(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            return redirect('appointmentlist')
    else:
        form = TestForm(instance=test)
    return render(request, 'testedit.html', {'form': form, 'test': test})

def testview(request):
    a=request.session.get('doctor_id')
    if not a:
        return redirect('landing')
    doc_id = request.session.get('doctor_id')
    doctor = get_object_or_404(Doctor, loginid=doc_id)
    tests = Test.objects.filter(doctor_id=doctor)
    return render(request, 'testview.html', {'tests': tests})   

def testdelete(request, id):
    test = get_object_or_404(Test, id=id)
    test.delete()
    return redirect('testview') 

def usertestview(request):
    a=request.session.get('user_id')
    if not a:
        return redirect('landing')
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, loginid=user_id)
    tests = Test.objects.filter(user_id=user)
    return render(request, 'usertestview.html', {'tests': tests})

def report(request,id):
    test = get_object_or_404(Test, id=id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=test)
        if form.is_valid():
            form.save()
            return redirect('usertestview')
    else:
        form = ReportForm(instance=test)
    return render(request, 'report.html', {'form': form})

def hospitalchat(request, receiver_id):
    hospital_login_id = request.session.get('hospital_id')
    hospital = get_object_or_404(Hospitalreg, loginid=hospital_login_id)
    sender = hospital.loginid
    receiver = get_object_or_404(Login, id=receiver_id)
    # Determine receiver name
    if Hospitalreg.objects.filter(loginid=receiver).exists():
        receiver_name = Hospitalreg.objects.get(loginid=receiver).hospital_name
    elif Ambulance.objects.filter(loginid=receiver).exists():
        receiver_name = Ambulance.objects.get(loginid=receiver).driver_name
    else:
        receiver_name = "Unknown"

    messages = Chat.objects.filter(
        Q(sender=sender, receiver=receiver) |
        Q(sender=receiver, receiver=sender)
    ).order_by('timestamp')

    # Mark received messages as read
    Chat.objects.filter(sender=receiver, receiver=sender, is_read=False).update(is_read=True)
    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            Chat.objects.create(sender=sender, receiver=receiver, chat=message)
            return redirect("hospitalchat", receiver_id=receiver_id)
    return render(request, "hospitalchat.html", {
        "messages": messages,
        "sender": sender,
        "receiver": receiver,
        "receiver_name": receiver_name
    })

def ambulancechatview(request):
    ambulance_id = request.session.get('ambulance_id')
    ambulance = get_object_or_404(Ambulance, loginid=ambulance_id)
    chats = Chat.objects.filter(
        Q(sender__id=ambulance.loginid.id) | Q(receiver__id=ambulance.loginid.id)
    ).order_by('timestamp')
    print(ambulance.loginid.id)
    return render(request, 'ambulancechatview.html', {'chats': chats})

def ambulancechatreply(request, id):
    chat = get_object_or_404(Chat, id=id)
    if request.method == 'POST':
        form = chatreplyForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            return redirect('ambulancechatview')
    else:
        form = chatreplyForm(instance=chat)
    return render(request, 'ambulance_chat_reply.html', {'form': form, 'chat': chat})

def doctor_availability_add(request):
    a=request.session.get('doctor_id')
    if not a:
      return redirect('landing')
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(loginid=doctor_id)
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor_id = doctor
            availability.save()
            return redirect('doctorhome')
    else:
        form = DoctorAvailabilityForm()
    return render(request, 'doctor_availability_add.html', {'form': form})

def doctor_availability_list(request):
    a=request.session.get('doctor_id')
    if not a:
      return redirect('landing')
    doctor_id = request.session.get('doctor_id')
    doctor= Doctor.objects.get(loginid=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor_id=doctor)
    return render(request, 'doctor_availability_view.html', {
        'availability': availability
    })

def doctor_availability_delete(request, id):
    availability = get_object_or_404(DoctorAvailability, id=id)
    availability.delete()
    return redirect('doctorhome')

def doctor_availability_edit(request, id):
    availability = get_object_or_404(DoctorAvailability, id=id)
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('doctorhome')
    else:
        form = DoctorAvailabilityForm(instance=availability)
    return render(request, 'doctor_availability_edit.html', {'form': form, 'availability': availability})

def user_view_doctor_availability(request, doctor_id):
    availability = DoctorAvailability.objects.filter(
        doctor_id=doctor_id,
        status=True
    )
    return render(request, 'user_doctor_availability.html', {
        'availability': availability
    })


def search_doctorsavailability(request):
    query = request.GET.get('q', '')
    specialization = request.GET.get('specialization', '')
    city = request.GET.get('city', '')
    doctors = Doctor.objects.all()
    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) |
            Q(specialization__icontains=query)
        )
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    if city:
        doctors = doctors.filter(city=city)
    # Get today’s availability for each doctor
    today = date.today()
    doctor_availability = {}
    for doctor in doctors:
        slots = DoctorAvailability.objects.filter(
            doctor_id=doctor,
            day=today,
            status=0  # Available
        )
        doctor_availability[doctor.id] = slots
    # Get distinct cities for dropdown
    cities = Doctor.objects.values_list('city', flat=True).distinct()
    context = {
        'doctors': doctors,
        'doctor_availability': doctor_availability,
        'query': query,
        'cities': cities,
    }
    return render(request, 'user_search_doctoravailability.html', context)

def doctor_patient_history_view(request,user_id):
    patient = get_object_or_404(User, id=user_id)
    appointments = Appointment.objects.filter(user_id=patient)
    return render(request, 'doctor patient history view .html', 
    {
        'appointments': appointments
    })

def About(request):
    return render(request, 'About.html')

def adminuserview(request):
    users = User.objects.all()
    return render(request, 'admin_userview.html', {'users': users})

def adminhospitallist(request):
    hospitals = Hospitalreg.objects.all()
    return render(request, 'adminhospitallist.html', {'Hospitalreg': hospitals})


def hospitalapprove(request, id):
    hospital = get_object_or_404(Hospitalreg, loginid__id=id)
    hospital.loginid.login_status = 1   # integer, not string
    hospital.loginid.save()
    return redirect('adminhospitallist')

def hospitalreject(request, id):
    hospital = get_object_or_404(Hospitalreg, loginid__id=id)
    hospital.loginid.login_status = 2
    hospital.loginid.save()
    return redirect('adminhospitallist')




# ===================================================================================================







from django.shortcuts import render
from PIL import Image
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
from serpapi import GoogleSearch
import os
from django.conf import settings

# Load model and processor only once
repo_name = "Jayanth2002/dinov2-base-finetuned-SkinDisease"
# Define a local cache directory to avoid permission issues in the default C:\Users\... path
cache_dir = os.path.join(settings.BASE_DIR, "hf_cache_v2")
os.makedirs(cache_dir, exist_ok=True)
image_processor = AutoImageProcessor.from_pretrained(repo_name, cache_dir=cache_dir)
model = AutoModelForImageClassification.from_pretrained(repo_name, cache_dir=cache_dir)
HIGH_SEVERITY = {
    "Melanoma",
    "Squamous Cell Carcinoma",
    "Basal Cell Carcinoma",
    # add any others you consider high risk…
}
# Your class names
class_names = [
    'Basal Cell Carcinoma', 'Darier_s Disease', 'Epidermolysis Bullosa Pruriginosa',
    'Hailey-Hailey Disease', 'Herpes Simplex', 'Impetigo', 'Larva Migrans',
    'Leprosy Borderline', 'Leprosy Lepromatous', 'Leprosy Tuberculoid', 'Lichen Planus',
    'Lupus Erythematosus Chronicus Discoides', 'Melanoma', 'Molluscum Contagiosum',
    'Mycosis Fungoides', 'Neurofibromatosis', 'Papilomatosis Confluentes And Reticulate',
    'Pediculosis Capitis', 'Pityriasis Rosea', 'Porokeratosis Actinic', 'Psoriasis',
    'Tinea Corporis', 'Tinea Nigra', 'Tungiasis', 'actinic keratosis', 'dermatofibroma',
    'nevus', 'pigmented benign keratosis', 'seborrheic keratosis',
    'squamous cell carcinoma', 'vascular lesion'
]
# SERPAPI KEY


SERPAPI_API_KEY = settings.SERPAPI_KEY


def search_serpapi(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    # First try to get a snippet from the answer box
    if "answer_box" in results and "snippet" in results["answer_box"]:
        snippet = results["answer_box"]["snippet"]
        link = results.get("answer_box", {}).get("link", "https://www.google.com/search?q=" + query)
        return snippet, link

    # Fallback to the first organic result
    elif "organic_results" in results and len(results["organic_results"]) > 0:
        first_result = results["organic_results"][0]
        snippet = first_result.get("snippet", "Information not found.")
        link = first_result.get("link", "https://www.google.com/search?q=" + query)
        return snippet, link

    # If nothing useful is found
    return "Information not found.", "https://www.google.com/search?q=" + query

from django.http import JsonResponse

from django.http import JsonResponse
import torch.nn.functional as F

def predict_skin_disease(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # 1) Load & preprocess
        image = Image.open(request.FILES['image']).convert("RGB")
        inputs = image_processor(images=image, return_tensors="pt")

        # 2) Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        # 3) Softmax → probs
        probs = F.softmax(logits, dim=-1)[0]
        confidence, idx = torch.max(probs, dim=0)
        confidence = confidence.item()
        idx        = idx.item()

        # 4) Threshold check
        THRESHOLD = 0.6
        if confidence < THRESHOLD:
            return JsonResponse({
                "error": "I’m not confident this is a skin lesion.",
                "confidence": confidence
            })

        # 5) Valid prediction
        predicted_class = class_names[idx]

        # 6) Severity check
        if predicted_class in HIGH_SEVERITY:
            return JsonResponse({
                "predicted_class": predicted_class,
                "confidence": round(confidence, 3),
                "alert": (
                  "⚠️ This appears to be a high-risk condition. "
                  "Please consult a dermatologist or healthcare professional as soon as possible."
                )
            })

        # 7) Fetch from web for non-high severity
        remedy_snippet, remedy_link     = search_serpapi(f"home remedy for {predicted_class}")
        medicine_snippet, medicine_link = search_serpapi(f"medicine for {predicted_class}")

        return JsonResponse({
            "predicted_class": predicted_class,
            "confidence": round(confidence, 3),
            "remedy": remedy_snippet,
            "remedy_link": remedy_link,
            "medicine": medicine_snippet,
            "medicine_link": medicine_link
        })

    return render(request, 'skinpredict.html')


def save_disease(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        disease_text = request.POST.get("disease", "").strip()
        if disease_text:
            appointment.disease = disease_text
            appointment.save()
    return redirect("appointmentlist")




import random

def search_tips_for_disease(topic="general skin care"):
    params = {
        "engine": "google",
        "q": f"tips for {topic}",
        "api_key": SERPAPI_API_KEY,
        "num": 10,  # fetch more results to have more variety
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])

    tips = []
    links = []

    for res in results:
        snippet = res.get("snippet")
        link = res.get("link")
        if snippet:
            tips.append(snippet)
            links.append(link)

    if not tips:
        return {
            "tips": "📝 No skin care tips found at the moment. Try asking later!",
            "link": "#"
        }

    # Randomly pick 2-3 tips each time
    selected_tips = random.sample(tips, min(3, len(tips)))
    # Randomly pick one source link from available links
    selected_link = random.choice(links) if links else "#"

    return {
        "tips": " ".join(selected_tips),
        "link": selected_link
    }

def search_products_for_disease(topic="skin care", num_results=8):
    # domains = ["sephora.com", "ulta.com", "amazon.com", "nykaa.com", "maccosmetics.com","boots.com", "netmeds.com", "1mg.com", "pharmeasy.in", "dermstore.com"]
    # query = f"best products for {topic}"
    query = f"best products for {topic} skin treatment"


    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results,
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("shopping_results", [])

    products = []
    for r in results:
        # link = r.get("link", "")
        # if not any(domain in link for domain in domains):
        #     continue

        products.append({
            "title": r.get("title"),
            "snippet": r.get("snippet", ""),
            "link":    r.get("link") or r.get("product_link", "#"),
            "image":   r.get("thumbnail") or None,
            "price":   r.get("price", ""),
            "source":  r.get("source", ""),
        })
        if len(products) >= num_results:
            break

    return products



def recommended_products(request):
    user_master = Login.objects.get(id=request.session["user_id"])
    reg=get_object_or_404(User,loginid=user_master)
    appts = Appointment.objects.filter(user_id=reg, disease__isnull=False)
    diseases = {a.disease.strip() for a in appts if a.disease}

    recommendations = []
    for disease in diseases:
        # FIXED — passes the actual diagnosed condition
        products = search_products_for_disease(topic=disease)
        tips_info = search_tips_for_disease(topic=disease)
        recommendations.append({
            "disease": disease,          # ← add this
            "products": products,
            "tips": tips_info["tips"],
            "tips_link": tips_info["link"]
        })

    return render(request, 'recommended_products.html', {
        "recommendations": recommendations
    })

def fetch_products_from_serpapi(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_API_KEY,  # replace with your actual API key
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    products = []
    for product in results.get("shopping_results", []):
        products.append({
            "title": product.get("title"),
            "link": product.get("link") or product.get("product_link"),  # <-- fallback to product_link
            "price": product.get("price"),
            "thumbnail": product.get("thumbnail"),
        })

    return products
def personalized_products(request):
    
    user_master = Login.objects.get(id=request.session["user_id"])

    userinfo = User.objects.get(loginid=user_master)

    query = f"skin care products for {userinfo.skin_type} skin for {'men' if userinfo.gender == 'M' else 'women'}"

    products = fetch_products_from_serpapi(query)

    return render(request, "personalized_products.html", {
        "products": products
    })


import math
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Hospitalreg, Emergency

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlmb/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))


def hospital_emergencies_api(request):
    login_id = request.session.get("hospital_id")
    hospital = Hospitalreg.objects.filter(loginid=login_id).first()

    if not hospital:
        return JsonResponse({"error": f"Hospital not found for session loginid={login_id}"}, status=400)

    if not hospital.latitude or not hospital.longitude:
        return JsonResponse({"error": "Hospital location not set. Please update your profile."}, status=400)

    radius_km = float(request.GET.get("radius", 10))
    hours = int(request.GET.get("hours", 24))
    since = timezone.now() - timedelta(hours=hours)

    qs = Emergency.objects.select_related("p_id").filter(date__gte=since).order_by("-date")

    emergencies = []
    for e in qs:
        try:
            dist = haversine_km(hospital.latitude, hospital.longitude, e.latitude, e.longitude)
        except (ValueError, TypeError):
            continue  # skip emergencies with bad lat/lng data
        if dist <= radius_km:
            emergencies.append({
                "id": e.id,
                "lat": float(e.latitude),
                "lng": float(e.longitude),
                "created_at": e.date.strftime("%Y-%m-%d %H:%M:%S"),  # ← fixed key name
                "distance_km": round(dist, 2),
                "patient_name": e.p_id.name,
                "patient_contact": e.p_id.contact,
            })

    return JsonResponse({
        "hospital": {
            "lat": float(hospital.latitude),
            "lng": float(hospital.longitude),
            "name": hospital.hospital_name  # fixed: was hos_name or hname
        },
        "radius_km": radius_km,
        "count": len(emergencies),
        "emergencies": emergencies
    })

def hospital_emergency_map(request):
    login_id = request.session.get("hospital_id")
    hospital = get_object_or_404(Hospitalreg, loginid=login_id)
    return render(request, "hospital_emergency_map.html", {"hospital": hospital})



# Emergency



def emergency(request):
    a = request.session.get('user_id')
    b = get_object_or_404(User, loginid=a)
    if request.method == "POST":
        lat = request.POST.get("latitude")
        lng = request.POST.get("longitude")
        if not lat or not lng:
            messages.error(request, "Location is required to send an emergency alert.")
            return render(request, "emergency.html", {})
        Emergency.objects.create(
            p_id=b,
            latitude=lat,
            longitude=lng
        )
        return redirect("userhome")
    return render(request, "emergency.html", {})


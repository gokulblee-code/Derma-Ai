from django import forms

from .models import *





GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

STATE_CHOICES = (
    ('Kerala', 'Kerala'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Karnataka', 'Karnataka'),
)

DISTRICT_CHOICES = (
    ('Ernakulam', 'Ernakulam'),
    ('Trivandrum', 'Trivandrum'),
    ('Kozhikode', 'Kozhikode'),
    ('Thrissur', 'Thrissur'),
    ('Palakkad', 'Palakkad'),
    
)

SPECIALIZATION_CHOICES = [
    ('Cardiology', 'Cardiology'),
    ('Neurology', 'Neurology'),
    ('Orthopedics', 'Orthopedics'),
    ('Dermatology', 'Dermatology'),
    ('Pediatrics', 'Pediatrics'),
    ('General Medicine', 'General Medicine'),
    ('ENT', 'ENT'),
    # Add more as needed
]

# Define your choices at the top of forms.py
VEHICLE_TYPE_CHOICES = [
    ('Basic Life Support', 'Basic Life Support'),
    ('Advanced Life Support', 'Advanced Life Support'),
    ('Patient Transport', 'Patient Transport'),
    ('Neonatal Ambulance', 'Neonatal Ambulance'),
]

CATEGORY_CHOICES = [
    ('Emergency', 'Emergency'),
    ('Non-Emergency', 'Non-Emergency'),
    ('VIP', 'VIP'),
    ('Other', 'Other'),
]

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control with-icon',
                'placeholder': 'Email',
                'style': 'padding-left: 40px;',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control with-icon',
                'placeholder': 'Password',
                'style': 'padding-left: 40px;',
            }),
        }
    
    


class UpdateLoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control with-icon',
                'placeholder': 'Email',
                'style': 'padding-left: 40px;',
            }),
       
            
            
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'contact']
    
    

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospitalreg
        fields = ['hospital_name', 'address', 'state', 'district', 'city', 'contact', 'latitude', 'longitude']
        widgets = {
            'hospital_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Hospital Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Complete Address', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter City'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number', 'type': 'tel'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override state & district AFTER super()
        self.fields['state'] = forms.ChoiceField(
            choices=STATE_CHOICES,
            widget=forms.Select(attrs={'class': 'form-select'}),
            initial=getattr(self.instance, 'state', '')
        )
        self.fields['district'] = forms.ChoiceField(
            choices=DISTRICT_CHOICES,
            widget=forms.Select(attrs={'class': 'form-select'}),
            initial=getattr(self.instance, 'district', '')
        )

class CustomloginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'appointment-date'
        }),
        label="Appointment Date"
    )
    
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'id': 'appointment-time'
        }),
        label="Appointment Time"
    )
    
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        # No need for widgets in Meta since we defined them in the form fields above

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['prescription']
        widgets = {
            'prescription': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter prescription details...',
                'rows': 10,
                'cols': 40
            }),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['account_holder_name', 'cardno', 'cvv', 'expiry']

class ComplaintForm(forms.ModelForm):
    complaint = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,  # More rows for better UX
            'placeholder': 'Please describe your complaint in detail. Include relevant dates, times, and any reference numbers if applicable.',
            'style': 'resize: vertical;'  # Allow vertical resize only
        }),
        label="Complaint Details",
        help_text="Please be as specific as possible"  # Optional help text
    )

    class Meta:
        model = Complaint
        fields = ['complaint']

class ComplaintReplyForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Type your reply here...',
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'reply': 'Your Reply'
        }

class FeedbackForm(forms.ModelForm):
        class Meta:
            model = Feedback
    # Main feedback field
            fields = ['feedback']
            widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Please provide detailed feedback about your experience...',
            'style': 'resize: vertical; min-height: 200px;'
        })

# class HospitalForm(forms.ModelForm):
#     class Meta:
#         model = Hospitalreg
#         fields = ['hospital_name', 'address', 'state', 'district', 'city', 'contact']
        
class AmbulanceForm(forms.ModelForm):
    # Dropdown for type
    type = forms.ChoiceField(
        choices=VEHICLE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Dropdown for category
    catageory = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Ambulance
        fields = ['catageory', 'type', 'vechile_number', 'driver_name', 'hospital', 'contact']
        widgets = {
            'vechile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Vehicle Number'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Driver Name'}),
        
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number', 'type': 'tel'}),
        }     
class AssignForm(forms.ModelForm):
    assign_date = forms.DateField(
        widget=forms.DateInput(attrs={
            
            'type': 'date',
        }),
   
    )
    assign_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
           
            'type': 'time',
        }),
    )
    class Meta:
        model = Assign
        fields = ['address', 'assign_date', 'assign_time']

class ChatForm(forms.ModelForm):
    chat = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your message here...'
        }),
        label="Message"
    )
    class Meta:
        model = Chat
        fields = ['chat']

class chatreplyForm(forms.ModelForm):
    reply = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your reply here...'
        }),
        label="Reply"
    )
    class Meta:
        model = Chat
        fields = ['reply']

class DoctorForm(forms.ModelForm):

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    district = forms.ChoiceField(
        choices=DISTRICT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Add specialization choices
    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Doctor
        fields = [
            'name', 'dob', 'gender', 'state', 'district', 'city',
            'hospital_name', 'address', 'experience', 'specialization',
            'qualification', 'contact', 'consultationfee'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'consultationfee': forms.NumberInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test']
        widgets = {
            'test': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter test details...',
                'rows': 6
            }),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['report']
        widgets = {
            'report': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

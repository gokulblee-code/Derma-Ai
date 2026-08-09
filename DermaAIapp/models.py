from django.db import models

# Create your models here.
class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    user_type = models.CharField(max_length=20)
    login_status =models.IntegerField(default=0)

class User(models.Model):
    SKIN_TYPE_CHOICES = [
        ("dry", "Dry"),
        ("oily", "Oily"),
        ("combination", "Combination"),
        ("sensitive", "Sensitive"),
        ("normal", "Normal"),
    ]
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    gender = models.CharField(max_length=10,null=True, blank=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

class Doctor(models.Model):
    name = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100)
    contact = models.CharField(max_length=30)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    consultationfee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    availability = models.IntegerField(default=0)

class Appointment(models.Model):
    doctor_id =models.ForeignKey(Doctor,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    current_date = models.DateField(auto_now_add=True)
    prescription= models.TextField(max_length=500)
    Payment_status=models.IntegerField(default=0)
    consultationfee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    url = models.URLField(null=True)
    disease=models.CharField(max_length=1000, null=True, blank=True)


class Payment(models.Model):
    Appointmentid = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=200) 
    cardno =models.CharField(max_length=20)
    cvv=models.CharField(max_length=4)
    expiry=models.CharField(max_length=20)
    current_date=models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

class Complaint(models.Model):
    complaint = models.TextField(max_length=500)
    current_date = models.DateField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500, null=True, blank=True) 

class Feedback(models.Model):
    feedback = models.TextField(max_length=500)
    current_date = models.DateField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)

class Hospitalreg(models.Model):
    hospital_name = models.CharField(max_length=200)
    address = models.TextField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact = models.IntegerField()
    loginid = models.ForeignKey(Login,on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)


    def __str__(self):
        return f"{self.hospital_name}"


class Emergency(models.Model):
    date=models.DateTimeField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    p_id=models.ForeignKey(User,on_delete=models.CASCADE)

class Ambulance(models.Model):
    catageory= models.CharField(max_length=200)
    type= models.CharField(max_length=200)
    vechile_number= models.CharField(max_length=10)
    driver_name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospitalreg, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.CharField(max_length=15)
    loginid = models.ForeignKey(Login,on_delete=models.CASCADE,null=True,blank=True)
    availability = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.vechile_number}"
    
class Assign(models.Model):
  address = models.CharField(max_length=200)
  assign_date = models.DateField()
  assign_time = models.TimeField()
  current_date = models.DateField(auto_now_add=True)
  user_loginid = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
  Ambulance_loginid = models.ForeignKey(Ambulance,on_delete=models.CASCADE,null=True,blank=True)
  h_loginid=models.ForeignKey(Hospitalreg, on_delete=models.CASCADE,null=True,blank=True)
  status = models.IntegerField(default=0)

class Chat(models.Model):
    sender = models.ForeignKey(Login, on_delete=models.CASCADE,related_name='send_messages')
    receiver = models.ForeignKey(Login, on_delete=models.CASCADE,related_name='received_messages')
    chat = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reply = models.TextField(max_length=500, null=True, blank=True)
    def __str__(self):
        return f"From {self.sender.email} to {self.receiver.email} - {self.chat[:30]}"
    
class Test(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Appointmentid = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    test = models.TextField()
    current_date = models.DateField(auto_now=True)
    report = models.FileField(upload_to='test_reports/', null=True, blank=True)

class DoctorAvailability(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.DateField()  # Monday, Tuesday, etc.
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.IntegerField(default=0)  # Available / Not



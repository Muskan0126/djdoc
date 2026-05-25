from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
# Create your models here.


string_regex =  RegexValidator(regex=r'^[a-zA-Z]+(?:\s[a-zA-Z]+)*$', message="Some special characters like (~!#^`'$|{}<>*) are not allowed.")
mobile_validate = RegexValidator(regex=r'^(\+91)?[6-9]\d{9}$',message='Enter a valid 10-digit mobile number')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators= [EmailValidator])
    first_name = models.CharField(null = True, blank = True, validators=[string_regex])
    last_name = models.CharField(null = True, blank = True, validators=[string_regex])
    phone_number = models.CharField(null =True, blank = True, validators=[mobile_validate])

    def __str__(self):
        return self.email
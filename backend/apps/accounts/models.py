from django.contrib.auth.base_user import BaseUserManager,AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone



#every objects.smth are defualt manager of django ,but we want our own manager 
class CustomUserManager(BaseUserManager):
    """becuase of the login(which is with the phone )we should have our custom manager """

    def create_user(self,phone_number,password=None,**extra_fields):# extra fields:additional user fields as keyword arguments
        """show the manager how create a user """
        if not phone_number:
            raise ValueError ("شماره تلقن الزامی است")
        user=self.model(phone_number=phone_number,**extra_fields)#self.model:the model which attached to,(User model here)
        user.set_password(password)
        user.save(using=self._db) # ihave one database but its a manager standard to write self.db
        return user
    
    def create_superuser(self,phone_number,password=None,**extra_fields)  :
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")


        if extra_fields.get("is_superuser") is not True:   #.get():if the key does not exist there is no error 
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phone_number,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    phone_number=models.CharField(max_length=20 , unique=True)

    first_name=models.CharField(max_length=20 ,blank=True)
    last_name=models.CharField(max_length=20 ,blank=True)
    email=models.EmailField(null=True ,blank=True)
    is_active=models.BooleanField(default=True)
    date_joined=models.DateField(default=timezone.now)
    is_staff=models.BooleanField(default=False)
    
    objects=CustomUserManager()

    USERNAME_FIELD = "phone_number" #default=user_name

    REQUIRED_FIELDS = [] #password,USERNAME_FIELD(which is phone_number now) for creatsuperuser
    is_phone_verified = models.BooleanField(default=False)
        
    

    def __str__(self):
            return self.phone_number    
class OTPRequest(models.Model):
    phone_number = models.CharField(max_length=15, db_index=True)
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    attempts = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at'] # Meta contains model-level configuration, not field definitions.
                                   # It applies to the whole model instead of a single field.

  
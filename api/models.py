from pyexpat import model
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import uuid

# CUSTOM USER MANAGER CLASS
class usermanager(BaseUserManager):

   def createuser(self, name, password, phno, **extra_fields):

      if not phno:
         raise ValueError('Phone Number Required')
      if not name:
         raise ValueError("Name Required")

      user = self.model(
         name = name,
         phno = phno,
         **extra_fields
      )

      user.set_password(password)
      user.save()
      return user

# USER MODEL
class User(AbstractBaseUser, PermissionsMixin):
   name = models.CharField(max_length=100)
   phno = models.CharField(max_length=15, unique=True, primary_key=True)
   email = models.CharField(max_length=100, blank=True, null=True)

   objects = usermanager()

   USERNAME_FIELD = "phno"
   REQUIRED_FIELDS = ["name"]

   def __str__(self):
      return self.name

# GLOBAL DATABASE
class Contacts(models.Model):
   id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
   name = models.CharField(max_length=100)
   phno = models.CharField(max_length=15)
   is_spam = models.BooleanField(default=False)
   whose_contact = models.ForeignKey(User, blank = True, null = True, on_delete=models.PROTECT)

   def __str__(self):
      return self.name
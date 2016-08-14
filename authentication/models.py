from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class AccountManager(BaseUserManager):
	def create_user(self, email, password=None, **kwargs):
		if not email:
			raise ValueError('Users must have a valid email.')

		if not kwargs.get('username'):
			raise ValueError('Users must have a username.')

		account = self.model(
				email =  self.normalize_email(email),
				username =  kwargs.get('username')
			)
		account.set_password(kwargs.get('password'))

		account.save()

		return account

	def create_superuser(self, email, password, **kwargs):
		account = self.create_user(email, password, **kwargs)
		account.is_admin = True

		account.save()
		return account 



class Account(AbstractBaseUser):
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=40,unique=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	tagline = models.CharField(max_length=144, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	is_admin = models.BooleanField(default=False)

	objects = AccountManager()

	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['username']

	def __unicode__(self):
		return self.email 

	def get_full_name(self):
		return ' '.join(self.first_name, self.last_name)

	def get_short_name():
		if self.first_name:
			return self.first_name
		else: return self.username



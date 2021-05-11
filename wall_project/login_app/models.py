from django.db import models
import re
import dateutil.parser
import datetime
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(form['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        
        return errors
    
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw,
        )
        
class TripManager(models.Manager):
     def validate(self, form):
        errors = {}
        if len(form['destination']) < 1:
            errors['destination'] = 'Empty destination is not allowed'
        if len(form['description']) < 1:
            errors['description'] = 'Empty description is not allowed'
        if len(form['start_date']) < 1:
            errors['start_date'] = 'Empty start date is not allowed'
        if len(form['end_date']) < 1:
            errors['end_date'] = 'Empty end date is not allowed'
        if 'start_date' in form and len(form['start_date'])> 1:
            start_date = dateutil.parser.parse(form['start_date'])
            end_date = dateutil.parser.parse(form['end_date'])
            if start_date < datetime.datetime.today():
                errors['start_date'] = 'Start date should be in the future'
            if start_date > end_date:
                errors['end_date'] = 'Start date can not be ahead of the end date'
        return errors



# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, related_name="created_trips", on_delete = models.CASCADE)
    travelers = models.ManyToManyField(User, related_name="trips")
    start_date = models.DateField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()


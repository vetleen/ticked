from datetime import datetime  

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Todo(models.Model):
	head_line = models.CharField(max_length=50, blank=True)
	body_text = models.CharField(max_length=300, blank=True)
	owner = models.ForeignKey(User)
	todo_is_ticked = models.BooleanField(default=False)
	date_created = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
	
	
	### These are unused now, but the idea is to implement this at a later stage ###
	
	#color_code is meant to be used to allow users to color code their todos
	color_code = models.CharField(max_length=50, blank=True)
	#deadline will be the date the user himself sets as the deadline
	deadline = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
	



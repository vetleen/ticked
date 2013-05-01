from django.db import models

# Create your models here.

class Todo(models.Model):
	head_line = models.CharField(max_length=50, blank=True)
	body_text = models.CharField(max_length=300, blank=True)
	owner = models.ForeignKey(User)
	todo_is_ticked = models.BooleanField(default=False)
	date_created = models.DateTimeField(default=datetime.now)
	
	
	### These are unused now, but the idea is to implement this at a later stage ###
	
	#color_code is meant to be used to allow users to color code their todos
	color_code = models.CharField(max_length=50, blank=True)
	#deadline will be the date the user himself sets as the deadline
	deadline = models.DateTimeField(default=datetime.now)
	#viewers are the other users who are allowed to view the todo
	todo_viewers = models.ManyToManyField(User)
	#todo_editors are the other users who are allowed to edit the todo
	todo_editors = models.ManyToManyField(User)
	#todo_tickers are the other users who are allowed to tick the todo
	todo_tickers = models.ManyToManyField(User)



from django.db import models

class Bean(models.Modsel):
	name = models.CharField(max_length=120)
	content = models.TextField()
	

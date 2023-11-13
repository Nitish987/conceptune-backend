from django.db import models
from django.conf import settings
from common.utils import generator


# Project Model
class Project(models.Model):
    id = models.CharField(default=generator.generate_identity, max_length=10, primary_key=True, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(default='', max_length=50)
    description = models.CharField(default='', max_length=200)
    envtype = models.CharField(default='DEVELOPMENT', choices=(('DEVELOPMENT', 'Development'), ('PRODUCTION', 'Production')), max_length=20)
    created_on = models.DateTimeField(auto_now=True)



# Project Apis Model
class ProjectApi(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.DO_NOTHING)
    api_key = models.CharField(default='', max_length=50)
    host = models.JSONField(default=list)
    created_on = models.DateTimeField(auto_now=True)
    
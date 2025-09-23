from django.db import models

# Create your models here.
class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True



class UserActionLog(AbstractBaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255)
    action_description = models.TextField()
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"
    

class Church(AbstractBaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500, null=True)
    town = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default="Kenya")
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    website = models.URLField(null=True)
    
    def __str__(self):
        return self.name
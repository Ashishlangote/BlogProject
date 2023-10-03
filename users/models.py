from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator

# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[mobile_regex], max_length=17,default="+911234567890")

    def __str__(self):
        # return f'{self.user.username} Profile'
        return f'{self.user.first_name} {self.user.last_name} Profile'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
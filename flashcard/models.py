from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="img/profile/", default="img/user_profile/user-profile-pic-solid.png")
    

class Folder(models.Model):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "folders")
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: 
        verbose_name = "Folder"
        verbose_name_plural = "Folders"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


class Set(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "sets")
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, related_name="sets", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: 
        verbose_name = "Set"
        verbose_name_plural = "Sets"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description" : self.description,
            "owner": self.owner.username,
            "folder": self.folder.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
    
class Card(models.Model):
    content = models.CharField(max_length=128)
    meaning = models.TextField()
    image = models.ImageField(upload_to='img/illustration/', blank=True)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name = "cards")
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name="cards")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "meaning": self.meaning,
            "image": self.image.url if self.image else None,
            "owner": self.owner.username,
            "set": self.set.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
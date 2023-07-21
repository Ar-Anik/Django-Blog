from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True,
                              error_messages={
                                  "unique": "Email Must Be Unique"
                              })
    profile_image = models.ImageField(upload_to="profile_images", null=True, blank=True)

    followers = models.ManyToManyField("Follow")

    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_profile_image(self):
        ImageUrl = ""
        try:
            ImageUrl = self.profile_image.url
        except:
            ImageUrl = ""

        return ImageUrl

class Follow(models.Model):
    followed = models.ForeignKey(User, related_name='user_followers', on_delete=models.CASCADE)    # jare follow korse
    followed_by = models.ForeignKey(User, related_name='user_follows', on_delete=models.CASCADE)   # je follow korese

    mute = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.followed_by.username} started following {self.followed.username}"



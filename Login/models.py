from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User


class song_album(models.Model):
       user = models.ForeignKey(User,default=1)
       artist = models.CharField(max_length=250)
       albub_title = models.CharField(max_length=250)
       genre = models.CharField(max_length=100)
       album_logo = models.FileField()
       is_favorite = models.BooleanField(default=False)

       def get_absolute_url(self):
           return reverse('Login:details',kwargs={'pk': self.pk})

       def __str__(self):
           return self.albub_title+' - '+self.artist

class song(models.Model):
    album=models.ForeignKey(song_album,on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file= models.FileField(default='')
    is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.song_title

from django.db import models

# Create your models here.


class Product(models.Model):
   TYPE_CHOICES = [
       ('L', 'Livre'),
       ('M', 'Musique'),
       ('V', 'Vidéo'),
   ]

   AGE_CHOICES = [
       ('Tout-petit', 'Tout-petit'),
       ('Petit', 'Petit'),
       ('Grand', 'Grand'),
       ('Tout-age', 'Tout-age'),
   ]

   nom = models.CharField(max_length=100)
   type = models.CharField(max_length=10, choices=TYPE_CHOICES)
   age = models.CharField(max_length=10, choices=AGE_CHOICES)
   file = models.FileField(upload_to='products/')
   cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)


   def __str__(self):
       return self.nom

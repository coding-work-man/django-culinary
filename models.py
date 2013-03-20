from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.mail import send_mail
from culinary.utils import *
from culinary.countries import CountryField

notify = False

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class IngredientAmount(models.Model):
    def __str__(self):
        return ('%s: %s' % (self.ingredient.name, self.amount))
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=100) # e.g, `250 ml.` or `1 kg`'

class Post(BaseModel):
    title = models.CharField(max_length=60)
    preview_picture = models.CharField(max_length=100) # Link for preview
    cuisine = CountryField() # e.g. `Russian` or `Japan`
    yields = models.PositiveSmallIntegerField() # e.g `Two big burgers`
    cooktime = models.PositiveSmallIntegerField() # e.g `About 30 minutes`
    description = models.TextField() # e.g `My favorite guilty pleasure breakfast`
    ingredients = models.ForeignKey(IngredientAmount) # e.g `Fish`
    body = models.TextField() # Content in the form of list of steps 
    serving_suggestions = models.TextField() # e.g `Serve immediately`
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Comment(BaseModel):
    author = models.CharField(max_length=60, blank=True)
    body = models.TextField()
    post = models.ForeignKey(Post, related_name="comments",  blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s" % (self.post, self.body[:60])

    def save(self, *args, **kwargs):
        """Email when a comment is added."""
        if notify:
            tpl = "Comment was was added to '%s' by '%s': \n\n%s"
            message = tpl % (self.post, self.author, self.body)
            from_addr = "no-reply@mydomain.com"
            recipient_list = ["myemail@mydomain.com"]
            send_mail("New comment added", message, from_addr, recipient_list)
        super(Comment, self).save(*args, **kwargs)
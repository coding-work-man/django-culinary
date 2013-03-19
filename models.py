from django.db.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.mail import send_mail
from culinary.utils import *
from culinary.countries import CountryField

notify = False

class DRYModel(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True # Abstract model for all objects

class Category(DRYModel):
    pass

class Ingredient(DRYModel):
    pass

class IngredientGroup(DRYModel):
    ingredients = models.ManyToManyField(Ingredient, through='IngredientAmount') # List of ingredients

class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    group = models.ForeignKey(IngredientGroup)
    amount = models.CharField(max_length=100) # e.g, `10 min` or `1.5 hour`
    amount_description = models.CharField(max_length=100) # e.g, `ml.` or `kg`

class Post(BaseModel):
    title = CharField(max_length=60)
    preview_picture = models.CharField(max_length=100) # Link for preview
    cuisine = CountryField() # e.g. `Russian` or `Japan`
    category = models.ForeignKey(Category) # e.g `Main dishes` or `Cocktails`
    yields = models.PositiveSmallIntegerField() # e.g `Two big burgers`
    cooktime = models.PositiveSmallIntegerField() # e.g `About 30 minutes`
    description = models.TextField() # e.g `My favorite guilty pleasure breakfast`
    content = models.TextField() # Content in the form of list of steps 
    serving_suggestions = models.TextField() # e.g `Serve immediately`
    created = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return self.title


class Comment(BaseModel):
    author = CharField(max_length=60, blank=True)
    body = TextField()
    post = ForeignKey(Post, related_name="comments",  blank=True, null=True)
    created = DateTimeField(auto_now_add=True)

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
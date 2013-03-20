from django.contrib import admin
from culinary.models import *

class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 0

class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    display_fields = "title created".split()

class CommentAdmin(admin.ModelAdmin):
    display_fields = "post author created".split()

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
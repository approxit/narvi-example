from django.contrib import admin

from words.models import Folder, Word


@admin.register(Folder, Word)
class WordsAdmin(admin.ModelAdmin):
    pass

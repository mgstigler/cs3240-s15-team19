from django.contrib import admin
from secure_witness.models import UserProfile, Media, Folder, File

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Media)
admin.site.register(Folder)
admin.site.register(File)
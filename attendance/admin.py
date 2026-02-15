from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

# @admin.register(FaceEmbedding)
# class FaceEmbeddingAdmin(admin.ModelAdmin):
#     list_display = ('user','created_at')

# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ('user','date','status','timestamp')

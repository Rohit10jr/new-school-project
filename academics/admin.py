from django.contrib import admin
from .models import *
# Register your models here.

class SubjectAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.is_anonymous:
            return True
        elif request.user.user_type == 'is_staff':
            return False

        elif request.user.user_type == 'is_admin':
            return True
class GradeAdmin(admin.ModelAdmin):
    def has_module_permission(self, request,obj=None):
        if request.user.is_anonymous:
            return True
        elif request.user.user_type == 'is_staff':
            return False
        elif request.user.user_type == 'is_admin':
            return True

admin.site.register(Answer)
admin.site.register(InstructionForTest)
admin.site.register(Questionbank)
admin.site.register(Grade,GradeAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Chapter)
admin.site.register(Question)
admin.site.register(Question_Paper)
admin.site.register(Test)
admin.site.register(TestResult)

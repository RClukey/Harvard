from django.contrib import admin
from .models import User, College, Question, Answer, Application, Question_Answer

# Register your models here.

admin.site.register(User)
admin.site.register(College)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Application)
admin.site.register(Question_Answer)
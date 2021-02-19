from django.contrib import admin
from .models import Question
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject'] # 장고 Admin에서 제목으로 질문을 검색할 수 있도록 검색 항목을 추가하자.

admin.site.register(Question)

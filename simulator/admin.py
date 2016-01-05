from django.contrib import admin
from .models import SimulatorTestResult, SimulatorTestItem
from .models import UploadFilename

# Register your models here.

class SimulatorTestItemInline(admin.StackedInline):
    model = SimulatorTestItem
    extra = 1

class SimulatorTestResultAdmin(admin.ModelAdmin):
    fields = ['test_user', 'test_record_time', 'test_comment',
            'test_result_detail_link']
    inlines = [SimulatorTestItemInline]
    list_display = ('test_user', 'test_record_time', 'test_comment',
            'test_result_detail_link')
    search_fields = ('test_user', 'test_comment')

class UploadFilenameAdmin(admin.ModelAdmin):
    fields = ['test_user', 'test_record_time', 'filename', 'test_comment',
            'test_result_detail_link']
    list_display = ['test_user', 'filename', 'test_record_time', 
            'test_comment', 'test_result_detail_link']
    search_fields = ('test_user', 'filename', 'test_comment')


admin.site.register(SimulatorTestResult, SimulatorTestResultAdmin)
admin.site.register(UploadFilename, UploadFilenameAdmin)

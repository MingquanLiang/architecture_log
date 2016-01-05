import os
from django.db import models
import django.utils.timezone as timezone

# Create your models here.

FLOATDEFAULT = -9.99

class SimulatorTestResult(models.Model):
    test_user = models.CharField('Test User', max_length=30)
    test_comment = models.CharField('Test Comment', max_length=100)
    test_record_time = models.DateTimeField('Record Test Result Time',
            default=timezone.now)
    test_result_detail_link = models.URLField('Test Result URL', 
            max_length=300)

    #def __unicode__(self):
    def __str__(self):
        return 'User:{0} | Record Time:{1}'.format(
                self.test_user, self.test_record_time)

class SimulatorTestItem(models.Model):
    """
    Because The Simulator Test Item Names are not determined, it should be 
    only a demo until now.
    """
    test_result = models.ForeignKey(SimulatorTestResult)
    test_time = models.DateTimeField('When Did The Test')
    test_type = models.CharField('Test Type(eg: L3, MCU, LSU etc.)', 
            max_length=20)
    test_configuration = models.CharField('Test Configuration', max_length=50)
    test_software = models.CharField('Tool for Test(eg: SpecCPU, Oprofile)', 
            max_length=20)

    test_item_IPC = models.FloatField('IPC Value', default = FLOATDEFAULT)
    test_item_memory_bandwidth = models.FloatField('Memory Bandwidth(MB/s)',
            default=FLOATDEFAULT)
    test_item_L1_miss_rate = models.FloatField('L1 Miss Rate(%)', 
            default=FLOATDEFAULT)
    test_item_reversed_one = models.FloatField('1st Reversed Item', 
            default=FLOATDEFAULT)
    test_item_reversed_two = models.FloatField('2nd Reversed Item', 
            default=FLOATDEFAULT)
    test_item_reversed_three = models.FloatField('3th Reversed Item', 
            default=FLOATDEFAULT)

    #def __unicode__(self):
    def __str__(self):
        return 'Test Type:{0} | Test Tool: {1} | Test Result:{2}'.format(
                self.test_type, self.test_software, self.test_time)


class UploadFilename(models.Model):
    test_user = models.CharField('Test User', max_length=30)
    test_comment = models.CharField('Test Comment', max_length=100)
    test_record_time = models.DateTimeField('Record Test Result Time')
    filename = models.FileField(upload_to='%Y-%m-%d/%H-%M-%S')
    test_result_detail_link = models.URLField('Test Result URL', 
            max_length=300)

    #def __unicode__(self):
    def __str__(self):
        return 'Test User:{0} | filename: {1} | Record Time:{2}'.format(
                self.test_user, os.path.basename(str(self.filename)), 
                self.test_record_time)


from django.contrib import admin

from .models import DataCachingInformation, DataCachingMachine
from .models import LmbenchInformation, LmbenchMachine
from .models import ParsecInformation, ParsecMachine
from .models import SiriusSuitInformation, SiriusSuitMachine
from .models import SparkInformation, SparkMachine
from .models import SpecCPUInformation, SpecCPUMachine
from .models import SpecjbbInformation, SpecjbbMachine
from .models import SpecjvmInformation, SpecjvmMachine
from .models import SplashInformation, SplashMachine
from .models import TpccInformation, TpccMachine
from .models import WebServingInformation, WebServingMachine


class BaseMachineInline(admin.StackedInline):
    fieldsets = [
            ('Machine Information', {
                'fields': (('machine_name', 'machine_side'),)
                }
                ),
            ('CPU Information', {
                'fields': (('architecture_type', 'byte_order'),)
                }
                ),
            ('Cache & Memory', {
                'fields': (('l1_instruction','l1_data','l2'),
                    ('l3', 'l4', 'memory'),)
                }
                ),
            ('Operation System', {
                'fields': (('os_type', 'kernel_version'),
                    'dependence_information')
                }
                ),
            ]


#######################################################################
class DataCachingMachineInline(BaseMachineInline):
    model = DataCachingMachine
    extra = 1


class DataCachingAdmin(admin.ModelAdmin):
    inlines = [DataCachingMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_max_rps',), ('version',
                    'record_result_time'), ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('data_scale','number_works','number_connections',
                    'number_threads', 'network_bandwidth'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class LmbenchMachineInline(BaseMachineInline):
    model = LmbenchMachine
    max_num = 1

class LmbenchAdmin(admin.ModelAdmin):
    inlines = [LmbenchMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_time',), ('version',
                    'record_result_time'), ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('app_name','problem_size', 'processor_number'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class ParsecMachineInline(BaseMachineInline):
    model = ParsecMachine
    max_num = 1

class ParsecAdmin(admin.ModelAdmin):
    inlines = [ParsecMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_time',), ('version', 'record_result_time'),
                    ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('app_name','thread_number'), ('input_set',
                'smt_number'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class SiriusSuitMachineInline(BaseMachineInline):
    new_cpu_information = ('CPU Information', {'fields':
        (('architecture_type', 'byte_order', 'cur_freq'),)
        })
    fieldsets = []
    for i in BaseMachineInline.fieldsets:
        if i[0] == 'CPU Information':
            fieldsets.append(new_cpu_information)
        else:
            fieldsets.append(i)

    model = SiriusSuitMachine
    max_num = 1


class SiriusSuitAdmin(admin.ModelAdmin):
    inlines = [SiriusSuitMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_run_time', 'result_passed',
                    'result_warnings', 'result_errors'),
                    ('version', 'record_result_time'), ('reference_link',),)
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('app_name','pthread_num','dataset_size'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class SparkMachineIncline(BaseMachineInline):
    model = SparkMachine
    max_num = 1


class SparkAdmin(admin.ModelAdmin):
    inlines = [SparkMachineIncline]
    fieldsets = (
            (None, {
                'fields': (('result_times',), ('version',
                    'record_result_time'),('reference_link',), )
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('data_size','parition_size','processor_number'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class SpecCPUMachineInline(BaseMachineInline):
    new_cpu_information = ('CPU Information', {'fields':
        (('architecture_type', 'byte_order', 'cpu_number', 'cpu_frequency'),
         ('threads_per_core', 'cores_per_socket', 'socket_number',
             'numa_nodes'), )
         })
    fieldsets = []
    for i in BaseMachineInline.fieldsets:
        if i[0] == 'CPU Information':
            fieldsets.append(new_cpu_information)
        else:
            fieldsets.append(i)

    model = SpecCPUMachine
    max_num = 1


class SpecCPUAdmin(admin.ModelAdmin):
    inlines = [SpecCPUMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_int_rate_ratio', 'result_fp_rate_ratio'),
                    ('version', 'record_result_time'), ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('benchmarks','copies', 'smt_number'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class SpecjbbMachineInline(BaseMachineInline):
    model = SpecjbbMachine
    max_num = 1

class SpecjbbAdmin(admin.ModelAdmin):
    inlines = [SpecjbbMachineInline]
    fieldsets = (
            (None, {
                #'fields': (('result_bops',), ('version', 'record_result_time'),)
                'fields': (('result_bops', 'jbb_attachment'),
                    ('version', 'record_result_time'), ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('app_name', 'jvm_parameter'), ('processor_number',
                    'jvm_instances', 'warehouses'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class SpecjvmMachineInline(BaseMachineInline):
    model = SpecjvmMachine
    max_num = 1


class SpecjvmAdmin(admin.ModelAdmin):
    inlines = [SpecjvmMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_bops', 'jvm_attachment'),
                    ('version', 'record_result_time'), ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('app_name', 'processor_number'),
                    ('jvm_parameter', 'specjvm_parameter'))
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class SplashMachineInline(BaseMachineInline):
    model = SplashMachine
    max_num = 1

class SplashAdmin(admin.ModelAdmin):
    inlines = [SplashMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_time',), ('version', 'record_result_time'),
                    ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('app_name','problem_size','processor_number'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class TpccMachineInline(BaseMachineInline):
    model = TpccMachine
    extra = 1
    max_num = 2

class TpccAdmin(admin.ModelAdmin):
    inlines = [TpccMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_tpmc',), ('version', 'record_result_time'),
                    ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('warehouses','terminals','network_bandwidth',
                    'run_time',),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )


#######################################################################
class WebServingMachineInline(BaseMachineInline):
    new_cache_information = ('Cache & Memory', {'fields':
        (('l1_instruction','l1_data','l2'),
         ('l3', 'half_l3', 'l4', 'memory'))
        })
    fieldsets = []
    for i in BaseMachineInline.fieldsets:
        if i[0] == 'Cache & Memory':
            fieldsets.append(new_cache_information)
        else:
            fieldsets.append(i)
    model = WebServingMachine
    extra = 1
    max_num = 3

class WebServingAdmin(admin.ModelAdmin):
    inlines = [WebServingMachineInline]
    fieldsets = (
            (None, {
                'fields': (('result_ops', 'result_passed', 'result_warnings',
                    'result_errors'), ('version', 'record_result_time'),
                    ('reference_link',))
                }
                ),
            ('Project Information', {
                'fields': (('project_name', 'project_id'),)
                }
                ),
            ('Configration', {
                'fields': (('warm_up', 'con_users', 'pm_static',
                    'pm_max_connections'), ('sql_max_connections',
                    'worker_connection','worker_processes',
                    'network_bandwidth'),)
                }
                ),
            ('Bottleneck (click for "yes")', {
                'fields': (('neck_cpu', 'neck_memory',
                    'neck_io', 'neck_net'),)
                }
                ),
            )

# register the models into admin
admin.site.register(DataCachingInformation, DataCachingAdmin)
admin.site.register(LmbenchInformation, LmbenchAdmin)
admin.site.register(ParsecInformation, ParsecAdmin)
admin.site.register(SiriusSuitInformation, SiriusSuitAdmin)
admin.site.register(SparkInformation, SparkAdmin)
admin.site.register(SpecCPUInformation, SpecCPUAdmin)
admin.site.register(SpecjbbInformation, SpecjbbAdmin)
admin.site.register(SpecjvmInformation, SpecjvmAdmin)
admin.site.register(SplashInformation, SplashAdmin)
admin.site.register(TpccInformation, TpccAdmin)
admin.site.register(WebServingInformation, WebServingAdmin)


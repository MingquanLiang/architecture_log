from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class ProjectInformation(models.Model):
    project_name = models.CharField('Project Name', max_length=32)
    project_id = models.CharField('Project ID', max_length=32)
    reference_link = models.URLField('Reference Link (Confluence)',
            default='http://10.100.8.185:8090')

    class Meta:
        abstract = True

class HardwareEnvironment(models.Model):
    Machine_Name_Choices = (
            #(None, 'Choose Machine Name'),
            ('Habonaro', 'Habonaro'),
            ('Palmetto', 'Palmetto'),
            ('S812L', 'S812L'),
            ('S822L', 'S822L'),
            ('X86_E5', 'X86 E5 Series'),
            )
    Architecture_Type_Choices = (
            #(None, 'Choose Architecture Type'),
            ('x86', 'x86'),
            ('powerpc', 'powerpc'),
            ('arm64', 'arm64'),
            ('mips', 'mips'),
            )
    Byte_Order_Choices = (
            #(None, 'Litter or Big Endian'),
            ('litter_endian', 'Litter Endian'),
            ('big_endian', 'Big Endian'),
            )
    Machine_Side_Choices = (
            #(None, 'Server or Client Side'),
            ('server_side', 'As a Server'),
            ('client_side', 'As a Client'),
            )

    machine_side = models.CharField('Server/Client',
            choices=Machine_Side_Choices, max_length=32, default='server_side'
            )
    machine_name = models.CharField('Machine Name',
            choices=Machine_Name_Choices, max_length=32, default='Habonaro'
            )
    cpu_type = models.CharField('CPU Type', max_length=16)
    architecture_type = models.CharField('Architecture',
            choices=Architecture_Type_Choices, max_length=32,
            default='powerpc',
            )
    byte_order = models.CharField('Litter or Big endian',
            choices=Byte_Order_Choices, max_length=32, default='big_endian'
            )
    l1_instruction = models.PositiveSmallIntegerField('L1 Instruction (KB)')
    l1_data = models.PositiveSmallIntegerField('L1 Data (KB)')
    l2 = models.PositiveSmallIntegerField('L2 Cache (KB)')
    l3 = models.PositiveIntegerField('L3 Cache (KB)', default=0, blank=True)
    l4 = models.PositiveIntegerField('L4 Cache (KB)', default=0, blank=True)
    memory = models.PositiveIntegerField('Memory (MB)')

    class Meta:
        abstract = True

class SoftwareEnvironment(models.Model):
    os_type = models.CharField('Operation System', max_length=64)
    kernel_version = models.CharField('Kernel Version', max_length=64)
    dependence_information = models.TextField('Dependency Instruction',
            max_length=1024, blank=True)

    class Meta:
        abstract = True

class Bottleneck(models.Model):
    neck_cpu = models.BooleanField('CPU Neck')
    neck_io = models.BooleanField('IO Neck')
    neck_memory = models.BooleanField('Memory Neck')
    neck_net = models.BooleanField('Net Neck')

    class Meta:
        abstract = True


APPLICATIONS = ('Data Caching', 'Lmbench', 'Parsec', 'Sirius', 'Spark Terasort',
        'SPEC CPU', 'SPEC jbb', 'SPEC jvm', 'Splash', 'TPCC', 'WebServing'
        )

#####################       Application From Here          ###################
##############################################################################
class DataCachingInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Data Caching',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_max_rps = models.DecimalField('Result - Max RPS', max_digits=12,
            decimal_places=4)
    data_scale = models.PositiveSmallIntegerField('Data Scale')
    number_works = models.PositiveSmallIntegerField('Work Number')
    number_connections = models.PositiveSmallIntegerField('Connection Number')
    number_threads = models.PositiveSmallIntegerField('Thread Number')
    network_bandwidth = models.PositiveSmallIntegerField('Network Bandwidth '
            '(Mbps)')

    def __str__(self):
        return "{0}: Max RPS={1} | Data Scale={2} | Works={3} | "\
    "Connections={4} | Threads={5} | Network Bandwidth={6}".format(
            self.test_application, self.result_max_rps, self.data_scale,
            self.number_works,self.number_connections, self.number_threads,
            self.network_bandwidth)

    class Meta:
        abstract = False


class DataCachingMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(DataCachingInformation,
            verbose_name='DataCaching Information')

    class Meta:
        abstract = False


##############################################################################
class LmbenchInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Lmbench',
            editable=False)
    version = models.CharField('Application Version', max_length = 10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.DecimalField('Result - Time', max_digits=12,
            decimal_places=4)
    app_name = models.CharField('app name', max_length=256, default='bw_mem')
    problem_size = models.CharField('Problem Size', max_length=256)
    node = models.CharField('Node', max_length=256)
    phycpu = models.CharField('Physical CPU', max_length=256)
    thread_number = models.PositiveSmallIntegerField('Thread Number')
    stride_size = models.PositiveIntegerField('Stride Size (Byte)')

    def __str__(self):
        return '{0}: Time={1} | app name={2} | Problem Size={3} | Processor'\
    ' Number={4}'.format(self.test_application, self.result_time, 
            self.app_name, self.problem_size, self.processor_number)

    class Meta:
        abstract = False


class LmbenchMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(LmbenchInformation,
            verbose_name='Lmbench Information')

    class Meta:
        abstract = False


##############################################################################
class ParsecInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Parsec',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.DecimalField('Result - Time', max_digits=12,
            decimal_places=4)
    app_name = models.CharField('app name', max_length=256)
    input_set = models.CharField('Input Set', max_length=256)
    thread_number = models.PositiveSmallIntegerField('Thread Number')
    smt_number = models.PositiveSmallIntegerField('SMT')

    def __str__(self):
        return '{0}: Time={1} | app name={2} | Input Set={3} | Threads={4} |'\
    ' SMT={5}'.format(self.test_application, self.result_time, self.app_name,
            self.input_set, self.thread_number, self.smt_number)

    class Meta:
        abstract = False

class ParsecMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(ParsecInformation,
            verbose_name='Parsec Information')

    class Meta:
        abstract = False


##############################################################################
class SiriusSuitInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Sirius-suit',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_run_time = models.DecimalField('Result - RUN_TIME', max_digits=12,
            decimal_places=4)
    result_passed = models.BooleanField('Result - PASSED')
    result_warnings = models.BooleanField('Result - WARNINGS')
    result_errors = models.BooleanField('Result - ERRORS')
    app_name = models.CharField('app name', max_length=256)
    pthread_num = models.PositiveSmallIntegerField('Pthread Number')
    dataset_size = models.DecimalField('Dataset Size (GB)', max_digits=12,
            decimal_places=4)

    def __str__(self):
        return '{0}: Run Time{1} | PASSED={2} | WARNINGS={3} | ERRORS={4} | '\
    'app name={5} | Pthread={6} | Dataset={7} GB'.format(
            self.test_application, self.result_run_time, self.result_passed,
            self.result_warnings, self.result_errors, self.app_name,
            self.pthread_num, self.dataset_size)

    class Meta:
        abstract = False


class SiriusSuitMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    cur_freq = models.DecimalField('CUR_FREQ (GHZ)', max_digits=8,
            decimal_places=4)
    app_information = models.ForeignKey(SiriusSuitInformation,
            verbose_name='Sirius-suit Information')

    class Meta:
        abstract = False


##############################################################################
class SparkTerasortInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Spark Terasort',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_times = models.DecimalField('Result - Time(s)', max_digits=12,
            decimal_places=4)
    #TODO: what base unit ??? MB or GB?
    data_size = models.DecimalField('Data Size (GB)', max_digits=12,
            decimal_places=4)
    parition_size = models.PositiveSmallIntegerField('Partition Size')
    processor_number = models.PositiveSmallIntegerField('Processor Number')

    def __str__(self):
        return '{0}: Time(s)={1} | Data Size={2} | Partition Size={3} | '\
    'Processor Number={4}'.format(self.test_application, self.result_times,
            self.data_size, self.parition_size, self.processor_number)

    class Meta:
        abstract = False

class SparkTerasortMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SparkTerasortInformation,
            verbose_name='SparkTerasort Information')
    class Meta:
        abstract = False


##############################################################################
class SpecCPUInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='SPEC CPU',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_int_rate_ratio = models.DecimalField("Result - INT Rate Ratio's",
            max_digits=12, decimal_places=4)
    result_fp_rate_ratio = models.DecimalField("Result - FP Rate Ratio's",
            max_digits=12, decimal_places=4)
    benchmarks = models.CharField("Benchmarks", max_length=256)
    #processor_number = models.PositiveSmallIntegerField("Processor Number")
    #TODO: change processor_number into copies and add smt_number
    copies = models.PositiveSmallIntegerField('Copies')
    smt_number = models.PositiveSmallIntegerField('SMT')

    def __str__(self):
        return "{0}: INT Rate Ratio's={1} | FP Rate Ratio's={2} |"\
    " Benchmarks={3} | Copies={4} | SMT={5}".format(self.test_application,
            self.result_int_rate_ratio, self.result_fp_rate_ratio,
            self.benchmarks, self.copies, self.smt_number)

    class Meta:
        abstract = False

class SpecCPUMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    #TODO: add some new fields
    threads_per_core = models.PositiveSmallIntegerField('Thread(s) Per Core')
    cores_per_socket = models.PositiveSmallIntegerField('Core(s) Per Socket')
    socket_number = models.PositiveSmallIntegerField('Socket(s)')
    numa_nodes = models.PositiveSmallIntegerField('NUMA Node(s)')
    cpu_number = models.PositiveSmallIntegerField('CPU(s)')
    cpu_frequency = models.DecimalField('CPU Clock Frequency (GHZ)',
            max_digits=8, decimal_places=4)
    app_information = models.ForeignKey(SpecCPUInformation,
            verbose_name='SPEC CPU Information')

    class Meta:
        abstract = False


##############################################################################
class SpecjbbInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Spec jbb',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='2005')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_bops = models.DecimalField('Result - bops', max_digits=12,
            decimal_places=4)
    #TODO: add for upload file
    jbb_attachment = models.FileField(upload_to = '%Y-%m-%d/%H-%M-%S',
            blank=True)

    app_name = models.CharField('app name', max_length=256)
    processor_number = models.PositiveSmallIntegerField('Processor Number')
    jvm_parameter = models.CharField('JVM Parameter', max_length=512,
            blank=True)
    jvm_instances = models.PositiveSmallIntegerField('JVM Instances',
            blank=True)
    warehouses = models.PositiveIntegerField('WAREHOUSES', blank=True)

    def __str__(self):
        return '{0}: app name={1} | JVM Parameter={2} | Processor(s)={3} | '\
    'JVM Instances={4} | WAREHOUSES={5}'.format(self.test_application,
            self.app_name, self.jvm_parameter, self.processor_number,
            self.jvm_instances, self.warehouses)

    class Meta:
        abstract = False


class SpecjbbMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SpecjbbInformation,
            verbose_name='Specjbb Information')

    class Meta:
        abstract = False


##############################################################################
class SpecjvmInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Spec jvm',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='2008')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_bops = models.DecimalField('Result - bops', max_digits=12,
            decimal_places=4)
    jvm_attachment = models.FileField(upload_to = '%Y-%m-%d/%H-%M-%S',
            blank=True)
    app_name = models.CharField('app name', max_length=256)
    jvm_parameter = models.CharField('JVM Parameter', max_length=512)
    specjvm_parameter = models.CharField('Spec JVM Parameter', max_length=512)
    processor_number = models.PositiveSmallIntegerField('Processor Number')

    def __str__(self):
        return '{0}: bops={1} | app name={2} | JVM Parameter={3} | '\
    'Spec JVM Parameter={4} | processor_number={5}'.format(self.test_application, self.result_bops,
            self.app_name, self.jvm_parameter, self.specjvm_parameter, self.processor_number)

    class Meta:
        abstract = False

class SpecjvmMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SpecjvmInformation,
            verbose_name='Specjvm Information')

    class Meta:
        abstract = False


##############################################################################
class SplashInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='Splash',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='2.0')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_time = models.DecimalField('Result - Time', max_digits=12,
            decimal_places=4)
    app_name = models.CharField('app name', max_length=256)
    problem_size = models.CharField('Problem Size', max_length=256)
    processor_number = models.PositiveSmallIntegerField('Processor Number')

    def __str__(self):
        return '{0}: Time={1} | app name={2} | Problem Size={3} | '\
    'Processor={4}'.format(self.test_application, self.result_time,
            self.app_name, self.problem_size, self.processor_number)

    class Meta:
        abstract = False

class SplashMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(SplashInformation,
            verbose_name='Splash Information')

    class Meta:
        abstract = False


##############################################################################
class TpccInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='TPC-C',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_tpmc = models.DecimalField('Result - tpmC', max_digits=12,
            decimal_places=4)
    warehouses = models.PositiveIntegerField('WAREHOUSES')
    terminals = models.PositiveSmallIntegerField('TERMINALS')
    run_time = models.DecimalField('RUN_TIME', max_digits=12,
            decimal_places=4)
    network_bandwidth = models.PositiveSmallIntegerField('Network Bandwidth '
            '(Mbps)')

    def __str__(self):
        return '{0}: tpmC={1} | WAREHOUSES={2} | TERMINALS={3} | Run '\
        'Time={4} | Network Bandwidth={5}'.format(self.test_application,
        self.result_tpmc, self.warehouses, self.terminals, self.run_time,
            self.network_bandwidth)

    class Meta:
        abstract = False

class TpccMachine(HardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(TpccInformation,
            verbose_name='TPC-C Information')

    class Meta:
        abstract = False

##############################################################################
class WebServingInformation(ProjectInformation, Bottleneck):
    test_application = models.CharField(max_length=32, default='WebServing',
            editable=False)
    version = models.CharField('Application Version', max_length=10,
            default='0.1')
    record_result_time = models.DateTimeField('Record Result Time',
            default=timezone.now)

    result_ops = models.DecimalField('Result - OPS', max_digits=12,
            decimal_places=4)
    result_passed = models.BooleanField('Result - PASSED')
    result_warnings = models.BooleanField('Result - WARNINGS')
    result_errors = models.BooleanField('Result - ERRORS')
    warm_up = models.PositiveSmallIntegerField('Warm Up')
    con_users = models.PositiveSmallIntegerField('CON Users')
    pm_static = models.BooleanField('PM Staic')
    pm_max_connections = models.PositiveSmallIntegerField('PM Max Connections')
    sql_max_connections = models.PositiveSmallIntegerField(
            'SQL Max Connections')
    #TODO: add some new fields
    worker_processes = models.PositiveSmallIntegerField('Worker Processes')
    worker_connection = models.PositiveSmallIntegerField('Worker Connection')
    network_bandwidth = models.PositiveSmallIntegerField('Network Bandwidth '
            '(Mbps)')

    def __str__(self):
        return '{0}: OPS={1} | PASSED={2} | WARNINGS={3} | ERRORS={4} | Warm'\
    ' Up={5} | CON Users={6} | PM Staic={7} | PM Max Connections={8} | '\
    'Worker Processes={9} | Worker Connection={10} | Network '\
    'Bandwidth={11}'.format(self.test_application, self.result_ops,
            self.result_passed, self.result_warnings, self.result_errors,
            self.warm_up, self.con_users, self.pm_static,
            self.pm_max_connections, self.worker_processes,
            self.worker_connection, self.network_bandwidth)

    class Meta:
        abstract = False


class WebServingHardwareEnvironment(models.Model):
    Machine_Name_Choices = (
            #(None, 'Choose Machine Name'),
            ('Habonaro', 'Habonaro'),
            ('Palmetto', 'Palmetto'),
            ('S812L', 'S812L'),
            ('S822L', 'S822L'),
            ('X86_E5', 'X86 E5 Series'),
            )
    Architecture_Type_Choices = (
            #(None, 'Choose Architecture Type'),
            ('x86', 'x86'),
            ('powerpc', 'powerpc'),
            ('arm64', 'arm64'),
            ('mips', 'mips'),
            )
    Byte_Order_Choices = (
            #(None, 'Litter or Big Endian'),
            ('litter_endian', 'Litter Endian'),
            ('big_endian', 'Big Endian'),
            )
    Machine_Side_Choices = (
            ('frontend', 'As a Frontend'),
            ('backend', 'As a Backend'),
            ('client_side', 'As a Client'),
            )



    #TODO: django1.8 Can not override the field
    """
    There is a link about "Field name “hiding” is not permitted"
    https://docs.djangoproject.com/en/dev/topics/db/models/#field-name-hiding-is-not-permitted
    """
    machine_side = models.CharField('Machine Role',
            choices=Machine_Side_Choices, max_length=32, default='client_side'
            )
    machine_name = models.CharField('Machine Name',
            choices=Machine_Name_Choices, max_length=32, default='Habonaro'
            )
    cpu_type = models.CharField('CPU Type', max_length=16)
    architecture_type = models.CharField('Architecture',
            choices=Architecture_Type_Choices, max_length=32,
            default='powerpc'
            )
    byte_order = models.CharField('Litter or Big endian',
            choices=Byte_Order_Choices, max_length=32, default='big_endian'
            )
    l1_instruction = models.PositiveSmallIntegerField('L1 Instruction (KB)')
    l1_data = models.PositiveSmallIntegerField('L1 Data (KB)')
    l2 = models.PositiveSmallIntegerField('L2 Cache (KB)')
    l3 = models.PositiveIntegerField('L3 Cache (KB)', default=0, blank=True)
    half_l3 = models.BooleanField('Half L3 Cache')
    l4 = models.PositiveIntegerField('L4 Cache (KB)', default=0, blank=True)
    memory = models.PositiveIntegerField('Memory (MB)')

    class Meta:
        abstract = True


class WebServingMachine(WebServingHardwareEnvironment, SoftwareEnvironment):
    last_modify_time = models.DateTimeField('Last Modified Time',
            auto_now=True)
    app_information = models.ForeignKey(WebServingInformation,
            verbose_name='WebServing Information')

    class Meta:
        abstract = False




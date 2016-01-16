import sys
import datetime
import copy

from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import ProjectInformation
from .models import HardwareEnvironment
from .models import DataCachingInformation as dc_i, DataCachingMachine as dc_m
from .models import LmbenchInformation as lb_i, LmbenchMachine as lb_m
from .models import ParsecInformation as pa_i, ParsecMachine as pa_m
from .models import SiriusSuitInformation as ss_i, SiriusSuitMachine as ss_m
from .models import SparkTerasortInformation as st_i, SparkTerasortMachine as st_m
from .models import SpecCPUInformation as scpu_i, SpecCPUMachine as scpu_m
from .models import SpecjbbInformation as sjbb_i, SpecjbbMachine as sjbb_m
from .models import SpecjvmInformation as sjvm_i, SpecjvmMachine as sjvm_m
from .models import SplashInformation as spl_i, SplashMachine as spl_m
from .models import TpccInformation as tpc_i, TpccMachine as tpc_m
from .models import WebServingInformation as ws_i, WebServingMachine as ws_m
from .models import WebServingHardwareEnvironment as ws_h


project_names = [ i[0] for i in ProjectInformation.Project_Name_Choices ]
architectures = [ i[0] for i in HardwareEnvironment.Architecture_Type_Choices ]
cpu_types = [ i[0] for i in ProjectInformation.CPU_Type_Choices ]

class ApplicationBaseInformation(object):
    """
    This class store base information related to all applications include:
    "datacaching, lmbench, parsec, siriussuit, sparkterasort, speccpu,
    specjbb, specjvm, splash, tpcc and webserving".
    """
    def __init__(self):
        self.applications = ['datacaching', 'lmbench', 'parsec', 'siriussuit',
                'sparkterasort', 'speccpu', 'specjbb', 'specjvm', 'splash',
                'tpcc', 'webserving',
                ]
        self.app_infor = {}
        self.app_infor['datacaching'] = {
                'information_module': dc_i,
                'machine_module': dc_m,
                'range_fields': ('data_scale', 'number_works',
                    'number_connections', 'number_threads'),
                'choice_fields': ('network_bandwidth',),
                'result_fields': ('result_max_rps', ),
                'result_alias_fields' : ('data_scale', 'number_works',
                    'number_connections', 'number_threads', 
                    'network_bandwidth', 'reference_link', ),
                }
        self.app_infor['lmbench'] = {
                'information_module': lb_i,
                'machine_module': lb_m,
                'range_fields': ('thread_number', ),
                'choice_fields': ('node', 'phycpu', 'stride_size'),
                'result_fields': ('result_time', ),
                'result_alias_fields' : ('thread_number', 'node', 'phycpu',
                    'stride_size', 'reference_link', ),
                }
        self.app_infor['parsec'] = {
                'information_module': pa_i,
                'machine_module': pa_m,
                'range_fields': None,
                'choice_fields': ('thread_number', ),
                'result_fields': ('result_time', ),
                'result_alias_fields' : ('thread_number', 'result_time', 
                    'reference_link', ),
                }
        self.app_infor['siriussuit'] = {
                'information_module': ss_i,
                'machine_module': ss_m,
                'range_fields': ('dataset_size', ),
                'choice_fields': ('app_name', 'pthread_num'),
                'result_fields': ('result_run_time', ),
                'result_alias_fields': ('reference_link', 'result_passed', 
                    'result_warnings', 'result_errors'),
                }
        self.app_infor['sparkterasort'] = {
                'information_module': st_i,
                'machine_module': st_m,
                'range_fields': ('data_size', 'parition_size', 'workers'),
                'choice_fields': ('processor_number', ),
                'result_fields': ('result_time', ),
                'result_alias_fields' : ('data_size', 'parition_size',
                    'workers', 'processor_number', 'reference_link', ),
                }
        self.app_infor['speccpu'] = {
                'information_module': scpu_i,
                'machine_module': scpu_m,
                'range_fields': None,
                'choice_fields': ('copies', ),
                # TODO: more than one result fields.
                'result_fields': ('result_int_rate_ratio',
                    'result_fp_rate_ratio', ),
                'result_alias_fields' : ('copies','reference_link', ),
                }
        self.app_infor['specjbb'] = {
                'information_module': sjbb_i,
                'machine_module': sjbb_m,
                'range_fields': None,
                'choice_fields': ('jvm_parameter','jvm_instances','warehouses'),
                'result_fields': ('result_bops', ),
                'result_alias_fields' : ('jvm_parameter','jvm_instances', 
                    'warehouses', 'reference_link', ),
                }
        self.app_infor['specjvm'] = {
                'information_module': sjvm_i,
                'machine_module': sjvm_m,
                'range_fields': None,
                'choice_fields': ('jvm_parameter', 'specjvm_parameter'),
                'result_fields': ('result_bops', ),
                'result_alias_fields' : ('jvm_parameter', 'specjvm_parameter',
                    'reference_link', ),
                }
        self.app_infor['splash'] = {
                'information_module': spl_i,
                'machine_module': spl_m,
                'range_fields': None,
                'choice_fields': ('problem_size', ),
                'result_fields': ('result_time', ),
                'result_alias_fields' : ('problem_size', 'reference_link', ),
                }
        self.app_infor['tpcc'] = {
                'information_module': tpc_i,
                'machine_module': tpc_m,
                'range_fields': ('warehouses', 'terminals'),
                'choice_fields': None,
                'result_fields': ('result_tpmc', ),
                'result_alias_fields' : ('warehouses', 'terminals', 
                    'reference_link', ),
                }
        self.app_infor['webserving'] = {
                'information_module': ws_i,
                'machine_module': ws_m,
                'range_fields': None,
                'choice_fields': None,
                'result_fields': ('result_ops', ),
                'result_alias_fields': ('reference_link', 'result_passed', 
                    'result_warnings', 'result_errors'),
                }


class SearchIndexView(generic.TemplateView):
    """
    This view is inherited from generic.TemplateView and achieve:
    1.get base information related to all applications from models system;
    2.get all search input items and corresponding data which is from db;
    """
    template_name = 'performance/search/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchIndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SearchIndexView, self).get_context_data(**kwargs)

        # get all applications base information from configuration
        apps_base_infors_object = ApplicationBaseInformation()
        applications = apps_base_infors_object.applications
        apps_base_infors = apps_base_infors_object.app_infor

        app_infors = {}
        for app in applications:
            app_infors[app] = self.get_models_information(
                    apps_base_infors[app]['information_module'],
                    apps_base_infors[app]['range_fields'],
                    apps_base_infors[app]['choice_fields'],
                    )
        # FIXME: webserving should be handled differently
        app_infors['webserving'] = self.get_webserving_information()

        # render the context to template system
        ctx['project_names'] = project_names
        ctx['architectures'] = architectures
        ctx['cpu_types'] = cpu_types
        ctx['applications'] = applications
        ctx['app_infors'] = app_infors
        return ctx

    def get_webserving_information(self):
        """
        webserving filter condition:
        # filter: 1) machine_side=backend && architecture_type
        #         2) machine_side=frontend && half_l3=True/False
        #         3) machine_side=backend && half_l3=True/False
        """
        app_data = {}
        app_data['architecture_type'] = [ i[0] for i in
                ws_h.Architecture_Type_Choices ]
        app_data['machine_side'] = [ i[0] for i in ws_h.Machine_Side_Choices ]
        app_data['half_l3'] = [True, False]
        return app_data

    def get_limit_value(self, module_info, field_name):
        field_value_list = [ i.__getattribute__(field_name) for i in
                module_info ]
        return (min(field_value_list), max(field_value_list))

    def get_all_value(self, module_info, field_name):
        field_value_list = list(set([ i.__getattribute__(field_name) for i in
                module_info ]))
        return sorted(field_value_list)

    def get_gaps_value_list(self, min_one, max_one, segment_number=5):
        value_range = max_one - min_one
        if value_range <= segment_number:
            #segment_number = 2
            return [(min_one, max_one)]
        #gaps_value = value_range // segment_number
        gaps_value = value_range / segment_number
        #gaps_list = [min_one + gaps_value * i if i < segment_number else 
        #        max_one for i in range(segment_number+1)]
        gaps_list = []
        previous_one = min_one
        for i in range(1, segment_number):
            next_one = min_one + i * gaps_value
            gaps_list.append((previous_one, next_one))
            previous_one = 1 + next_one
        gaps_list.append((previous_one, max_one))
        return gaps_list

    def get_models_information(self, module_name, range_field_list=None,
            choice_field_list=None):
        """
        get the value range by looking for the value of field_name 
        in the module. such as: 
        app_data['data_scale'] = [(10, 20), (21, 30), (31, 40)]
        app_data['network_bandwidth'] = [1000, 2000, 4000, 5000, 8000,10000]
        """
        app_data = {}
        if module_name.objects.exists():
            module_info = [ i for i in module_name.objects.all() ]
        else:
            print("Still no data in {0}".format(module_name))
            if range_field_list:
                for field_name in range_field_list:
                    app_data[field_name] = [(0,0)]
            if choice_field_list:
                for field_name in choice_field_list:
                    app_data[field_name] = ["no data"]
            return app_data
        if range_field_list is not None:
            for field_name in range_field_list:
                min_field_value, max_field_value = self.get_limit_value(
                        module_info, field_name)
                app_data[field_name] = self.get_gaps_value_list(min_field_value, 
                        max_field_value)
        if choice_field_list is not None:
            for field_name in choice_field_list:
                app_data[field_name] = self.get_all_value(module_info,
                        field_name)
        return app_data


class SearchResultView(generic.TemplateView):
    """
    1. Get the post options and search data from db.
    2. show filtered data into table or figure
    """
    #template_name = 'performance/search/result.html'

    def __init__(self, **kwargs):
        super(SearchResultView, self).__init__(**kwargs)
        # get all applications base information from configuration
        self.apps_base_infors_object = ApplicationBaseInformation()
        self.applications = self.apps_base_infors_object.applications
        self.apps_base_infors = self.apps_base_infors_object.app_infor
        # The template_name should be determined by user submission
        self.template_name = 'performance/search/result_error.html'

    def get_same_element_in_list(self, list_former, list_latter):
        return list(set(list_former).intersection(list_latter))

    def get_all_field_name(self, module_name, exclude_list=()):
        field_name_list = [ field.name for field in module_name._meta.fields 
                if field.name not in exclude_list ]
        return field_name_list

    def get_all_field_verbose_name(self, module_name, exclude_list=()):
        """
        Still use field.name in exclude_list because field.name is stored
        in db which is more stable.
        """
        field_verbose_name_list = [ field.verbose_name for field in
                module_name._meta.fields if field.name not in exclude_list]
        return field_verbose_name_list

    def convert_string_to_tuple(self, string_name):
        trans_map = str.maketrans('(),', '   ')
        string_list = string_name.translate(trans_map).strip().split()
        min_one = float(string_list[0])
        max_one = float(string_list[1])
        return (min_one, max_one)

    def filter_needed_id(self, module_info, field_value_map, flag, 
            filter_field='id'):
        record_id_list = []
        for record_info in module_info:
            record_id = record_info.__getattribute__(filter_field)
            record_id_flag = True
            for field_name, field_value in field_value_map.items():
                record_field_value = record_info.__getattribute__(field_name)
                if flag == "choice":
                    if record_field_value != field_value:
                        # This record should be satisified with all options
                        record_id_flag = False
                        break
                elif flag == "range":
                    if ( record_field_value < field_value[0] ) or ( 
                            record_field_value > field_value[1] ):
                        record_id_flag = False
                        break
            if record_id_flag:
                record_id_list.append(record_id)
        return record_id_list

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchResultView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SearchResultView, self).get_context_data(**kwargs)
        ctx['kwargs'] = kwargs
        return ctx

    def post(self, request, *args, **kwargs):
        # the context being rendered store into kwargs
        kwargs = {}
        # FIXME: webserving can NOT use this post !!!!!!
        all_post_data = request.POST

        # base search items
        post_display_form = all_post_data.get('display_as')
        post_project_name = all_post_data.get('project_names')
        post_begin_time = all_post_data.get('begin_time')
        post_end_time = all_post_data.get('end_time')
        post_cpu_type = all_post_data.get('cpu_types')
        post_architecture = all_post_data.get('architectures')
        post_application = all_post_data.get('applications')

        # further search items related to application name
        post_app_i_module = self.apps_base_infors[
                post_application]['information_module']
        post_app_m_module = self.apps_base_infors[
                post_application]['machine_module']
        post_app_range_field_list = self.apps_base_infors[post_application][
                'range_fields']
        post_app_choice_field_list = self.apps_base_infors[post_application][
                'choice_fields']


        # get all chosen options of user and extract filter condition - start
        base_search_item_value_map = {}
        further_search_item_value_map = {}
        base_search_item_value_map['project_name'] = post_project_name
        base_search_item_value_map['cpu_type'] = post_cpu_type
        base_search_item_value_map['architecture'] = post_architecture
        base_search_item_value_map['application'] = post_application
        base_search_item_value_map['begin_time'] = post_begin_time
        base_search_item_value_map['end_time'] = post_end_time
        post_begin_time_format = datetime.datetime.strptime(post_begin_time,
                '%Y-%m-%d %H:%M:%S')
        post_end_time_format = datetime.datetime.strptime(post_end_time,
                '%Y-%m-%d %H:%M:%S')

        # get needed record from XXXInformation module
        i_filter_kwargs = {}
        i_filter_kwargs['project_name__exact'] = post_project_name
        i_filter_kwargs['cpu_type__exact'] = post_cpu_type
        i_filter_kwargs['record_result_time__range'] = (post_begin_time_format,
                post_end_time_format)
        graph_x_field_list = []
        if post_app_range_field_list is not None:
            for i in post_app_range_field_list:
                field_value = all_post_data.get(i)
                if field_value != "all_options":
                    field_value = self.convert_string_to_tuple(all_post_data.get(i))
                    i_filter_kwargs['{0}__{1}'.format(i, "range")] = \
                        field_value
                    further_search_item_value_map[i] = field_value
                else:
                    further_search_item_value_map[i] = "ALL"
                    graph_x_field_list.append(i)
        if post_app_choice_field_list is not None:
            for i in post_app_choice_field_list:
                field_value = all_post_data.get(i)
                if field_value != "all_options":
                    i_filter_kwargs['{0}__{1}'.format(i, "exact")] = \
                        field_value
                    further_search_item_value_map[i] = field_value
                else:
                    further_search_item_value_map[i] = "ALL"
                    graph_x_field_list.append(i)

        i_module_needed_queryset = post_app_i_module.objects.filter(
                **i_filter_kwargs)
        i_id_list = [ record.id for record in i_module_needed_queryset ]

        # get needed record from XXXMachine module
        m_filter_kwargs = {}
        m_filter_kwargs['architecture_type__exact'] = post_architecture
        m_module_needed_queryset = post_app_m_module.objects.filter(
                **m_filter_kwargs)
        m_id_list = [ record.app_information_id for record in
                m_module_needed_queryset ]
        # merge same value because ForeignKey in .models
        id_list = self.get_same_element_in_list(i_id_list, m_id_list)
        # get all chosen options of user and extract filter condition - end
        #------------------------------------------------------------------#

        # public kwargs
        kwargs['base_search_item_value_map']=base_search_item_value_map
        kwargs['further_search_item_value_map']=further_search_item_value_map

        if post_display_form == "graph":
            if len(graph_x_field_list) != 1:
                self.template_name = 'performance/search/result_error.html'
                kwargs['graph_error_message'] = "graph_error"
            else:
                self.template_name = 'performance/search/result_graph.html'
                result_fields = self.apps_base_infors[
                        post_application]['result_fields']
                result_alias_fields = self.apps_base_infors[
                        post_application]['result_alias_fields']
                graph_x_field = graph_x_field_list[0]
                graph_y_field = result_fields[0]
                figure_needed_record_list = [ record for record in
                        i_module_needed_queryset.order_by(graph_x_field) 
                        if record.id in id_list ]
                result_fields_value_list = []
                for record in figure_needed_record_list:
                    result_x_value = record.__getattribute__(graph_x_field)
                    result_y_value = record.__getattribute__(graph_y_field)
                    result_fields_value_list.append((
                        result_x_value, result_y_value,
                        {i:record.__getattribute__(i) for i 
                            in result_alias_fields},))
                kwargs['graph_x_field'] = graph_x_field
                kwargs['graph_y_field'] = graph_y_field
                kwargs['result_fields_value_list'] = result_fields_value_list
        elif post_display_form == "figure":
            self.template_name = 'performance/search/result_figure.html'
            # FIXME: should be get all result fields in production.
            result_fields = self.apps_base_infors[
                    post_application]['result_fields']
            result_alias_fields = self.apps_base_infors[
                    post_application]['result_alias_fields']
            figure_needed_record_list = [ record for record in
                    i_module_needed_queryset.order_by('record_result_time') 
                    if record.id in id_list ]
            result_fields_value_list = []
            for record in figure_needed_record_list:
                result_x_value = 1000 * int(
                        record.record_result_time.strftime('%s'))
                result_y_value = record.__getattribute__(result_fields[0])
                result_fields_value_list.append((
                        result_x_value, {result_fields[0]: result_y_value}, 
                        {i:record.__getattribute__(i) for i 
                            in result_alias_fields},))
            kwargs['result_fields_value_list'] = result_fields_value_list
        elif post_display_form == "table":
            self.template_name = 'performance/search/result_table.html'
            i_field_name_list = self.get_all_field_name(post_app_i_module,
                    exclude_list=('test_application', 'record_result_time', ))
            m_field_name_list = self.get_all_field_name(post_app_m_module,
                    exclude_list=('dependence_information', 'last_modify_time',
                        'app_information'))
            i_field_verbose_name_list = self.get_all_field_verbose_name(
                    post_app_i_module, exclude_list=('test_application', 
                        'record_result_time', ))
            m_field_verbose_name_list = self.get_all_field_verbose_name(
                    post_app_m_module, exclude_list=('dependence_information', 
                        'last_modify_time', 'app_information'))

            record_value_list = []
            # when display as table, use id of i_module as keyword
            for id_value in sorted(id_list):
                i_record_list = [i for i in post_app_i_module.objects.filter(
                    id__exact=id_value)]
                m_record_list = [i for i in post_app_m_module.objects.filter(
                    app_information_id__exact=id_value)]
                i_record_value = [i_record_list[0].__getattribute__(field_name) for
                        field_name in i_field_name_list]
                # len(i_record_list) always == 1, but len(m_record_list) >= 1
                for m_record in m_record_list:
                    every_record_value = copy.deepcopy(i_record_value)
                    # FIXME:break i_module_info and m_module_info into two parts
                    every_record_value.append('    ')
                    for field_name in m_field_name_list:
                        every_record_value.append(m_record.__getattribute__(
                            field_name))
                    record_value_list.append(every_record_value)

            #kwargs['i_module_header'] = i_field_name_list
            #kwargs['m_module_header'] = m_field_name_list
            kwargs['i_module_header'] = i_field_verbose_name_list
            kwargs['m_module_header'] = m_field_verbose_name_list
            kwargs['record_value_list'] = record_value_list
        else:
            self.template_name = 'performance/search/result_error.html'

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ReportOutputView(generic.TemplateView):
    template_name = 'performance/search/report_output.html'

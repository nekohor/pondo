from .statisitician import Statistician
from .exporter import Exporter


def batch_stat(task_name, record_type, protocol_type,
               line, start_date, end_date):

    stats = Statistician(task_name, record_type, protocol_type)
    stats.batch_stat(line, start_date, end_date)


def current_stat(task_name, record_type, protocol_type, cur_dir):

    stats = Statistician(task_name, record_type, protocol_type)
    stats.current_stat(cur_dir)


def specific_stat(task_name, record_type, protocol_type, coil_ids):

    stats = Statistician(task_name, record_type, protocol_type)
    stats.specific_stat(coil_ids)


def batch_export(factor_names, record_type, protocol_type,
                 line, start_date, end_date):

    stats = Exporter(factor_names, record_type, protocol_type)
    stats.batch_export(line, start_date, end_date)


def current_export(factor_names, record_type, protocol_type, cur_dir):

    stats = Exporter(factor_names, record_type, protocol_type)
    stats.current_export(cur_dir)


def specific_export(factor_names, record_type, protocol_type,
                    coil_ids, max_num=1200):

    stats = Exporter(factor_names, record_type, protocol_type, max_num)
    stats.specific_export(coil_ids)

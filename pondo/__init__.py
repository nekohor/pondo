from .statisitician import Statistician


def batch_stat(task_name, record_type, line, start_date, end_date):

    stats = Statistician(task_name, record_type)
    stats.batch_stat(line, start_date, end_date)


def current_stat(task_name, record_type, cur_dir):

    stats = Statistician(task_name, record_type)
    stats.current_stat(cur_dir)


def specific_stat(task_name, record_type, coil_ids):

    stats = Statistician(task_name, record_type)
    stats.current_stat(coil_ids)

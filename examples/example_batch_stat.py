import pondo

# task_name = "process_control"
task_name = "five_precision"
task_name = "waviness_prediction"
line = 1580
start_date = 20200101
end_date = 20200101


def run():
    record_type = "mes"
    protocol_type = "tcp"

    pondo.batch_stat(task_name, record_type, protocol_type,
                     line, start_date, end_date)


run()

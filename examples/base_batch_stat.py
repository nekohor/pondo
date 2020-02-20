import pondo


task_name = "base"
line = 1580
start_date = 20200101
end_date = 20200131


def run():
    record_type = "mes"
    protocol_type = "tcp"

    pondo.batch_stat(task_name, record_type, protocol_type,
                     line, start_date, end_date)


run()

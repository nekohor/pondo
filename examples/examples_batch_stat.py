import pondo


task_name = "base"
record_type = "ledger"

line = 1580
start_date = 20191001
end_date = 20191001

pondo.batch_stat(task_name, record_type, line, start_date, end_date)

import pondo

record_type = "ledger"
protocol_type = "tcp"

line = 1580
factor_names = ["leveling{}".format(x) for x in range(1, 8)]
start_date = 20191101
end_date = 20191231

pondo.batch_export(factor_names, record_type, protocol_type,
                   line, start_date, end_date)

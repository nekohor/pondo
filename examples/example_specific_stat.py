import pondo
import pandas as pd
from profile import Profile
p = Profile()

# task_name = "wedge"
task_name = "waviness_prediction"


record_type = "mes"
protocol_type = "tcp"

# filename = "D:/NutCloudSync/work/topics/999others/20191118合钢起筋/coils.xlsx"
# filename = "D:/work_sync/999other/20200112_34007F5双边浪/sample.xlsx"
# filename = "E:/query_result/query_1580_cid_20190101_20191231_20200116_110601.xlsx"

filename = "D:/work_sync/999other/20190109浪形预测评估/coils.xlsx"
# filename = "D:/NutCloudSync/work/topics/001shape/002平整浪形跟踪/2号平整浪形跟踪记录.xlsx"


df = pd.read_excel(filename)


def run():
    pondo.specific_stat(task_name, record_type, protocol_type, df["coil_id"])


# p.runcall(run)
# p.print_stats()

run()

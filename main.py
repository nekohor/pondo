from pondo.api import ApiServer
from pondo.config import Registry
from pondo.database import DataBaseManager
# ApiServer.run()


# connection = DataBaseManager.get_database("qms")


# cursor = connection.cursor()
# cursor.execute("""
#         SELECT MAT_NO, NAME, DATA
#         FROM TB_CURVE_DATA
#         WHERE MAT_NO = :coil_id AND NAME = 'HSM2.WEDGE40'
#         """, coil_id="M19157502W")

# rows = cursor.fetchall()
# for row in rows:
#     print(str(row[2].read(), 'utf-8').split(","))
# cursor.close()

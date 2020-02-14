from datetime import datetime
import sys

sys.path.append('../..')

from common.helpers import convert_to_dict
from common.constants import PSQL_CUR, PSQL_CONN


class MiceDbQueries:
    @staticmethod
    def find_mouse(mouse_id):
        try:
            PSQL_CUR.execute("SELECT * FROM mice_mice WHERE id=%s", mouse_id)
            return convert_to_dict(PSQL_CUR.description, PSQL_CUR.fetchone())
        except Exception:
            return None

    @staticmethod
    def get_mouse_last_features(mouse_id):
        PSQL_CUR.execute("""
        SELECT * FROM analysis_micefeatures \
        WHERE mouse_id=%s \
        ORDER BY date DESC \
        LIMIT 1
        """, mouse_id)

        return convert_to_dict(PSQL_CUR.description, PSQL_CUR.fetchone())

    @staticmethod
    def insert_mouse_features(data, commit=True):
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()

        fields = ",".join(data.keys())
        values = list(data.values())
        formatter = ('%s,' * len(values))[:-1]

        queue = """INSERT INTO {table} ({fields}) VALUES ({formatter})""".format(
            table='analysis_micefeatures',
            fields=fields,
            formatter=formatter,
        )

        PSQL_CUR.execute(queue, tuple(values))

        if commit:
            PSQL_CONN.commit()

    @staticmethod
    def insert_mouse_last_image(mouse_id, image, commit=False):
        created_at = datetime.now()

        PSQL_CUR.execute(
            """
            INSERT INTO mice_micelastimages (mouse_id,image,created_at,updated_at)
            VALUES (%s,%s,%s,%s)
            ON CONFLICT (mouse_id) DO
            UPDATE SET image=%s,created_at=%s,updated_at=%s
            """,
            (mouse_id, image, created_at, created_at, image, created_at, created_at)
        )

        if commit:
            PSQL_CONN.commit()

    @staticmethod
    def insert_mouse_image(mouse_id, image, commit=True):
        created_at = datetime.now()

        PSQL_CUR.execute(
            """
            INSERT INTO mice_miceimages (mouse_id,image,created_at,updated_at)
            VALUES (%s,%s,%s,%s)
            """,
            (mouse_id, image, created_at, created_at)
        )

        if commit:
            PSQL_CONN.commit()

from datetime import datetime
import sys

sys.path.append('../..')

from common.helpers import convert_to_dict
from common.constants import PSQL_CUR, PSQL_CONN


class ExperimentsDbQueries:
    @staticmethod
    def write_experiment_watcher_container(experiment_id, container_id, commit=True):
        created_at = datetime.now()
        updated_at = datetime.now()
        values = [experiment_id, container_id, created_at, updated_at]

        queue = """
        INSERT INTO watchers_experimentwatchers (experiment_id,container,created_at,updated_at)
        VALUES (%s,%s,%s,%s)
        """

        PSQL_CUR.execute(queue, tuple(values))

        if commit:
            PSQL_CONN.commit()

    @staticmethod
    def find_experiment_container(experiment_id):
        PSQL_CUR.execute(
            "SELECT container FROM watchers_experimentwatchers WHERE experiment_id=%s",
            experiment_id
        )
        return convert_to_dict(PSQL_CUR.description, PSQL_CUR.fetchone())

    @staticmethod
    def find_experiment_cameras_ip(experiment_id, mouse_status):
        PSQL_CUR.execute(
            """
            SELECT mice_mice.id, cameras_cameras.ip FROM mice_mice
            INNER JOIN cameras_cameras ON mice_mice.camera_id=cameras_cameras.id
            WHERE mice_mice.experiment_id=%s AND mice_mice.status=%s
            """,
            (experiment_id, mouse_status)
        )
        return convert_to_dict(PSQL_CUR.description, PSQL_CUR.fetchall())

    @staticmethod
    def remove_experiment_watcher_container(experiment_id, container_id, commit=True):
        PSQL_CUR.execute(
            """
            DELETE FROM watchers_experimentwatchers
            WHERE experiment_id=%s AND container=%s
            """,
            (experiment_id, container_id)
        )

        if commit:
            PSQL_CONN.commit()

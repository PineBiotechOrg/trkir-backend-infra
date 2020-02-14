import os
import sys

from kafka import KafkaConsumer

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

from common.constants import KAFKA_SERVERS, KAFKA_SERVERS_TEXT, DECODE_FORMAT
from watchers.experiments.helpers.helpers import \
    create_container, \
    remove_container, \
    make_rpi_ips, \
    make_rpi_ids
from watchers.experiments.constants.experiments_db_queries import ExperimentsDbQueries
from watchers.common.constants.constants import \
    ConsumerGroups, \
    Topics, \
    MouseStatuses
from watchers.experiments.constants.constants import \
    ExperimentWatcherRequests, \
    RPI_IPS_ENV, \
    MOUSE_IDS_ENV, \
    KAFKA_SERVERS_ENV


def manage_experiments():
    """
    Here we receive streamed image from the RPI and send them to the next topics.
    """

    consumer = KafkaConsumer(
        Topics.ExperimentManager.value,
        bootstrap_servers=KAFKA_SERVERS,
        group_id=ConsumerGroups.ExperimentManager.value,
    )

    for msg in consumer:
        experiment_id = msg.key.decode(DECODE_FORMAT)
        request = msg.value.decode(DECODE_FORMAT)

        if request == ExperimentWatcherRequests.Create.value:
            experiment_mice = ExperimentsDbQueries.find_experiment_cameras_ip(
                experiment_id,
                MouseStatuses.Continue.value,
            )
            container = create_container(
                environment={
                    RPI_IPS_ENV: make_rpi_ips(experiment_mice),
                    MOUSE_IDS_ENV: make_rpi_ids(experiment_mice),
                    KAFKA_SERVERS_ENV: KAFKA_SERVERS_TEXT,
                }
            )
            ExperimentsDbQueries.write_experiment_watcher_container(
                experiment_id,
                container.id,
            )
        if request == ExperimentWatcherRequests.Remove.value:
            try:
                container_id = ExperimentsDbQueries.find_experiment_container(experiment_id)['container']
                remove_container(container_id)
                ExperimentsDbQueries.remove_experiment_watcher_container(
                    experiment_id,
                    container_id,
                )
            except:
                # no such container
                # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
                pass
        if request == ExperimentWatcherRequests.Update.value:
            # for now update is just removing and creating new container (with updated info)
            try:
                container_id = ExperimentsDbQueries.find_experiment_container(experiment_id)['container']
                remove_container(container_id)
                ExperimentsDbQueries.remove_experiment_watcher_container(
                    experiment_id,
                    container_id,
                )
            except Exception:
                # no such container
                # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
                pass

            experiment_mice = ExperimentsDbQueries.find_experiment_cameras_ip(
                experiment_id,
                MouseStatuses.Continue.value,
            )

            container = create_container(
                environment={
                    RPI_IPS_ENV: make_rpi_ips(experiment_mice),
                    MOUSE_IDS_ENV: make_rpi_ids(experiment_mice),
                    KAFKA_SERVERS_ENV: KAFKA_SERVERS_TEXT,
                }
            )

            ExperimentsDbQueries.write_experiment_watcher_container(
                experiment_id,
                container.id,
            )

    consumer.close()


if __name__ == "__main__":
    manage_experiments()

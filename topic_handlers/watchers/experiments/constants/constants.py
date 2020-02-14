from enum import Enum

import docker


RPI_IPS_ENV = 'RPI_IPS'
MOUSE_IDS_ENV = 'MOUSE_IDS'
KAFKA_SERVERS_ENV = 'KAFKA_SERVERS'

DOCKER_CLIENT = docker.from_env()

DOCKER_IMAGE_PATH = './experiment_watcher.tar'


class ExperimentWatcherRequests(Enum):
    Create = 'create'
    Remove = 'remove'
    Update = 'update'

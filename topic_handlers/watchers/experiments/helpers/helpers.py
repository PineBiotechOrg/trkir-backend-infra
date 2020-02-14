from docker.errors import APIError
from watchers.experiments.constants.constants import \
    DOCKER_CLIENT, \
    DOCKER_IMAGE_PATH


def make_rpi_ips(mice):
    return ','.join([mouse['ip'] for mouse in mice])


def make_rpi_ids(mice):
    return ','.join([str(mouse['id']) for mouse in mice])


def create_container(environment):
    with open(DOCKER_IMAGE_PATH, 'rb') as docker_image_file:
        image = DOCKER_CLIENT.images.load(docker_image_file)[0]

    container = DOCKER_CLIENT.containers.run(
        image=image.id,
        environment=environment,
        detach=True
    )
    return container


def remove_container(container_id):
    container = DOCKER_CLIENT.containers.get(container_id)
    try:
        container.stop()
        container.remove()
    except APIError:
        # TODO: logging https://tracker.yandex.ru/VPAGROUPDEV-907
        pass

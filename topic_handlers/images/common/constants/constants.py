from enum import Enum


class ImageFormats(Enum):
    JPG = '.jpg'


# TOPICS
class Topics(Enum):
    Broker = 'main_broker'
    Processor = 'processor'
    FeaturesMaker = 'features_maker'
    Saver = 'saver'


BROKER_PRODUCE_TOPICS = [Topics.Saver.value]


class ConsumerGroups(Enum):
    Broker = 'broker-consumer-group'
    Processor = 'processor-consumer-group'
    Saver = 'saver-consumer-group'
    FeaturesMaker = 'features-maker-consumer-group'


BUFFER_SEPARATOR = ','
PACKET_LENGTH = 164
PACKET_OFFSET = 4
IMG_HEIGHT = 240
IMG_WIDTH = 160

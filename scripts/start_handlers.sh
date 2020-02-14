#!/bin/bash

# TODO: пофиксить sleep и написать скрипт дожидания кафки https://tracker.yandex.ru/VPAGROUPDEV-870
sleep 60 * 60 * 24

## Watchers
#/usr/local/bin/python3 topic_handlers/watchers/experiments/experiments.py &
#
## Images
#/usr/local/bin/python3 topic_handlers/images/broker/broker.py &
#/usr/local/bin/python3 topic_handlers/images/processor/processor.py &
#/usr/local/bin/python3 topic_handlers/images/saver/saver.py &
#/usr/local/bin/python3 topic_handlers/images/features_maker/features_maker.py &

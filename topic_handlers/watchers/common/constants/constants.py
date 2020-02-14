from enum import Enum


# TOPICS
class Topics(Enum):
    ExperimentManager = 'experiment_manager'


class ConsumerGroups(Enum):
    ExperimentManager = 'experiment-manager-consumer-group'


class MouseStatuses(Enum):
    Create = 'create'
    Start = 'start'
    Continue = 'continue'
    Pause = 'pause'
    Completed = 'complete'

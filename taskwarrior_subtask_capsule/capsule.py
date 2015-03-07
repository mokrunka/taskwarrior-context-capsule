from taskwarrior_capsules.capsule import CommandCapsule
from taskwarrior_capsules.exceptions import CapsuleError


class Capsule(CommandCapsule):
    MIN_VERSION = '0.2'
    MAX_VERSION = '1.0'
    MIN_TASKWARRIOR_VERSION = '2.3'
    MAX_TASKWARRIOR_VERSION = '2.4.999'

    def handle(self, filter_args, extra_args, **kwargs):
        pass

class BootstrapError(Exception):
    "An error when bootstrapping a new controller"


class BootstrapInterrupt(BootstrapError):
    "The bootstrap was interrupted by the user"


class ControllerNotFoundException(Exception):
    "An error when a controller can't be found in juju's config"


class DeploymentFailure(Exception):
    "A failure from a deployed model"

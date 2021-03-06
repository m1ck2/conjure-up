from conjureup import controllers, juju, utils
from conjureup.app_config import app
from conjureup.consts import CUSTOM_PROVIDERS
from conjureup.models.provider import Localhost as LocalhostProvider
from conjureup.models.provider import SchemaErrorUnknownCloud, load_schema
from conjureup.telemetry import track_event, track_screen
from conjureup.ui.views.cloud import CloudView

from .common import BaseCloudController


class CloudsController(BaseCloudController):

    def __init__(self):
        self.view = None

    def finish(self, cloud):
        """ Load the selected cloud provider
        """
        self.cancel_monitor.set()

        if cloud in CUSTOM_PROVIDERS:
            app.provider = load_schema(cloud)
        else:
            app.provider = load_schema(juju.get_cloud_types_by_name()[cloud])

        try:
            app.provider.load(cloud)
        except SchemaErrorUnknownCloud:
            app.provider.cloud = utils.gen_cloud()

        if app.provider.model is None:
            app.provider.model = utils.gen_model()

        track_event("Cloud selection", app.provider.cloud, "")

        return controllers.use('credentials').render()

    def render(self):
        "Pick or create a cloud to bootstrap a new controller on"
        track_screen("Cloud Select")

        all_clouds = juju.get_clouds()
        compatible_clouds = juju.get_compatible_clouds()
        cloud_types = juju.get_cloud_types_by_name()
        # filter to only public clouds
        public_clouds = sorted(
            name for name, info in all_clouds.items()
            if info['defined'] == 'public' and
            cloud_types[name] in compatible_clouds)
        # filter to custom clouds
        # exclude localhost because we treat that as "configuring a new cloud"
        custom_clouds = sorted(
            name for name, info in all_clouds.items()
            if info['defined'] != 'public' and
            cloud_types[name] != 'localhost' and
            cloud_types[name] in compatible_clouds)

        excerpt = app.config.get(
            'description',
            "Where would you like to deploy?")

        self.view = CloudView(app,
                              public_clouds,
                              custom_clouds,
                              cb=self.finish)

        if 'localhost' in compatible_clouds:
            app.log.debug(
                "Starting watcher for verifying LXD server is available.")
            app.loop.create_task(
                self._monitor_localhost(
                    LocalhostProvider(),
                    self.view._enable_localhost_widget
                )
            )

        app.ui.set_header(
            title="Choose a Cloud",
            excerpt=excerpt
        )
        app.ui.set_body(self.view)
        app.ui.set_footer('Please press [ENTER] on highlighted '
                          'Cloud to proceed.')


_controller_class = CloudsController

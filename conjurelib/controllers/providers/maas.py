# Copyright (c) 2015 Canonical Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from conjurelib.ui.views import MaasProviderView
from conjurelib.models.providers import MaasProviderModel
from conjurelib.juju import Juju
from conjurelib.controllers.deploy import DeployController


class MaasProviderController:
    def __init__(self, common):
        self.common = common
        self.view = MaasProviderView(self.common,
                                     self.finish)
        self.model = MaasProviderModel

    def finish(self, result):
        """ Deploys to the maas provider
        """
        for k in result.keys():
            if k in self.model.config:
                self.model.config[k] = result[k].value
        Juju.create_environment(self.common['config']['juju_env'],
                                "maas",
                                self.model.to_yaml())
        DeployController(self.common).render()

    def render(self):
        self.common['ui'].set_header(
            title="MAAS Provider",
            excerpt="Enter your MAAS credentials to "
            "enable deploying to this provider."
        )
        self.common['ui'].set_body(self.view)
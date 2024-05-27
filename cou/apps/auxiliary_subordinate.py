#  Copyright 2023 Canonical Limited
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Auxiliary subordinate application class."""
from cou.apps.auxiliary import OVN, AuxiliaryApplication
from cou.apps.factory import AppFactory
from cou.apps.subordinate import SubordinateApplication


@AppFactory.register_application(["mysql-router", "ceph-dashboard"])
class AuxiliarySubordinateApplication(SubordinateApplication, AuxiliaryApplication):
    """Auxiliary subordinate application class."""


@AppFactory.register_application(["ovn-chassis"])
class OVNSubordinate(OVN, AuxiliarySubordinateApplication):
    """OVN subordinate application class."""

    def _check_ovn_support(self) -> None:
        """Check OVN version.

        :raises ApplicationError: When workload version is lower than 22.03.0.
        """
        OVNSubordinate._validate_ovn_support(self.workload_version)

    def upgrade_plan_sanity_checks(
        self, target: OpenStackRelease, units: Optional[list[Unit]]
    ) -> None:
        """Run sanity checks before generating upgrade plan.

        :param target: OpenStack release as target to upgrade.
        :type target: OpenStackRelease
        :param units: Units to generate upgrade plan, defaults to None
        :type units: Optional[list[Unit]], optional
        :raises ApplicationError: When application is wrongly configured.
        :raises HaltUpgradePlanGeneration: When the application halt the upgrade plan generation.
        :raises MismatchedOpenStackVersions: When the units of the app are running different
                                             OpenStack versions.
        """
        self._check_ovn_support()
        self._check_version_pinning()
        super().upgrade_plan_sanity_checks(target, units)


@AppFactory.register_application(["hacluster"])
class HACluster(AuxiliarySubordinateApplication):
    """HACluster application class."""

    # hacluster can use channels 2.0.3 or 2.4 on focal.
    # COU changes to 2.4 if the channel is set to 2.0.3
    multiple_channels = True

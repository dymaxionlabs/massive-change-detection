# -*- coding: utf-8 -*-

# Massive Change Detection is a QGIS 2 plugin that applies change detection
# algorithms on satellite imagery for building reports for urban planning.
# Copyright (C) 2018  Dymaxion Labs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


__author__ = 'Damián Silvani'
__date__ = '2018-06-26'
__copyright__ = '(C) 2018 by Dymaxion Labs'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MassiveChangeDetection class from file MassiveChangeDetection.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .massive_change_detection import MassiveChangeDetectionPlugin
    return MassiveChangeDetectionPlugin()

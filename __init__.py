# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MassiveChangeDetection
                                 A QGIS plugin
 Change detection tool
                              -------------------
        begin                : 2018-06-26
        copyright            : (C) 2018 by Dymaxion Labs
        email                : contact@dymaxionlabs.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Dymaxion Labs'
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

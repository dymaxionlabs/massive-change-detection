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
"""

__author__ = 'Dymaxion Labs'
__date__ = '2018-06-26'
__copyright__ = '(C) 2018 by Dymaxion Labs'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import sys
import inspect

from processing.core.Processing import Processing
from massive_change_detection_provider import MassiveChangeDetectionProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class MassiveChangeDetectionPlugin:

    def __init__(self):
        self.provider = MassiveChangeDetectionProvider()

    def initGui(self):
        Processing.addProvider(self.provider)

    def unload(self):
        Processing.removeProvider(self.provider)

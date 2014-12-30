# -*- coding: utf-8 -*-
"""
/***************************************************************************
 cesium
                                 A QGIS plugin
 cesium
                             -------------------
        begin                : 2014-05-14
        copyright            : (C) 2014 by geodrinx
        email                : geodrinx@gmail.com
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

def classFactory(iface):
    # load cesium class from file cesium
    from cesium import cesium
    return cesium(iface)

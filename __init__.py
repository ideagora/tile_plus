# -*- coding: utf-8 -*-
"""
/***************************************************************************
 tile_plus
                                 A QGIS plugin
 tile plus
                             -------------------
        begin                : 2018-07-15
        copyright            : (C) 2018 by geodose
        email                : geodose@gmail.com
        git sha              : $Format:%H$
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load tile_plus class from file tile_plus.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .tile_plus import tile_plus
    return tile_plus(iface)

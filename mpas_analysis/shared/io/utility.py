# This software is open source software available under the BSD-3 license.
#
# Copyright (c) 2018 Los Alamos National Security, LLC. All rights reserved.
# Copyright (c) 2018 Lawrence Livermore National Security, LLC. All rights
# reserved.
# Copyright (c) 2018 UT-Battelle, LLC. All rights reserved.
#
# Additional copyright and license information can be found in the LICENSE file
# distributed with this code, or at
# https://raw.githubusercontent.com/MPAS-Dev/MPAS-Analysis/master/LICENSE
"""
IO utility functions

Phillip J. Wolfram, Xylar Asay-Davis
"""

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import glob
import os
import random
import string
from datetime import datetime


def paths(*args):  # {{{
    """
    Returns glob'd paths in list for arbitrary number of function arguments.
    Note, each expanded set of paths is sorted.

    Parameters
    ----------
    *args : list
        A list of arguments to pass to ``glob.glob``

    Returns
    -------
    paths : list of str
        A list of file paths
    """
    # Authors
    # -------
    # Phillip J. Wolfram

    paths = []
    for aargs in args:
        paths += sorted(glob.glob(aargs))
    return paths  # }}}


def fingerprint_generator(size=12,
                          chars=string.ascii_uppercase + string.digits):  # {{{
    """
    Returns a random string that can be used as a unique fingerprint

    Parameters
    ----------
    size : int, optional
        The number of characters in the fingerprint

    chars : list of char, optional
        The fingerprint

    Returns
    -------
    fingerprint : str
        A random string

    Reference
    ---------
    http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    """
    # Authors
    # -------
    # Phillip J. Wolfram

    return ''.join(random.choice(chars) for _ in range(size))  # }}}


def make_directories(path):  # {{{
    """
    Make the given path if it does not already exist.

    Parameters
    ----------
    path : str
        the path to make

    Returns
    -------
    path : str
        the path unchanged
    """
    # Authors
    # -------
    # Xylar Asay-Davis

    try:
        os.makedirs(path)
    except OSError:
        pass
    return path  # }}}


def build_config_full_path(config, section, relativePathOption,
                           relativePathSection=None,
                           defaultPath=None):  # {{{
    """
    Get a full path from a base directory and a relative path

    Parameters
    ----------
    config : MpasAnalysisConfigParser object
        configuration from which to read the path

    section : str
        the name of a section in `config`, which must have an option
        ``baseDirectory``

    relativePathOption : str
        the name of an option in ``section`` of the relative path within
        ``baseDirectory`` (or possibly an absolute path)

    relativePathSection : str, optional
        the name of a section for ``relativePathOption`` if not ``section``

    defaultPath : str, optional
        the name of a path to return if the resulting path doesn't exist.

    Returns
    -------
    fullPath : str
        The full path to the given relative path within the given
        ``baseDirectory``
    """
    # Authors
    # -------
    # Xylar Asay-Davis

    if relativePathSection is None:
        relativePathSection = section

    subDirectory = config.get(relativePathSection, relativePathOption)
    if os.path.isabs(subDirectory):
        fullPath = subDirectory
    else:
        fullPath = '{}/{}'.format(config.get(section, 'baseDirectory'),
                                  subDirectory)

    if defaultPath is not None and not os.path.exists(fullPath):
        fullPath = defaultPath
    return fullPath  # }}}


def build_obs_path(config, component, relativePathOption,
                   relativePathSection=None):  # {{{
    """

    Parameters
    ----------
    config : MpasAnalysisConfigParser object
        configuration from which to read the path

    component : {'ocean', 'seaIce', 'iceberg'}
        the prefix on the ``*Observations`` section in ``config``, which must
        have an option ``obsSubdirectory``

    relativePathOption : str
        the name of an option in `section` of the relative path within
        ``obsSubdirectory`` (or possibly an absolute path)

    relativePathSection : str, optional
        the name of a section for ``relativePathOption`` if not
        ``<component>Observations``

    Returns
    -------
    fullPath : str
        The full path to the given relative path within the observations
        directory for the given component
    """
    # Authors
    # -------
    # Xylar Asay-Davis

    obsSection = '{}Observations'.format(component)
    if relativePathSection is None:
        relativePathSection = obsSection

    relativePath = config.get(relativePathSection, relativePathOption)
    if os.path.isabs(relativePath):
        fullPath = relativePath
    else:
        obsSubdirectory = config.get(obsSection, 'obsSubdirectory')
        if os.path.isabs(obsSubdirectory):
            fullPath = '{}/{}'.format(obsSubdirectory, relativePath)
        else:
            basePath = config.get('diagnostics', 'baseDirectory')
            fullPath = '{}/{}/{}'.format(basePath, obsSubdirectory,
                                         relativePath)

    return fullPath  # }}}


def check_path_exists(path):  # {{{
    """
    Raise an exception if the given path does not exist.

    Parameters
    ----------
    path : str
        Absolute path

    Raises
    ------
    OSError
        If the path does not exist
    """
    # Authors
    # -------
    # Xylar Asay-Davis

    if not (os.path.isdir(path) or os.path.isfile(path)):
        raise OSError('Path {} not found'.format(path))  # }}}


def get_files_year_month(fileNames, streamsFile, streamName):  # {{{
    """
    Extract the year and month from file names associated with a stream

    Parameters
    ----------
    fileNames : list of str
        The names of files with a year and month in their names.

    streamsFile : ``StreamsFile``
        The parsed streams file, used to get a template for the

    streamName : str
        The name of the stream with a file-name template for ``fileNames``

    Returns
    -------
    years, months : list of int
        The years and months for each file in ``fileNames``
    """
    # Authors
    # -------
    # Xylar Asay-Davis

    template = streamsFile.read_datetime_template(streamName)
    template = os.path.basename(template)
    dts = [datetime.strptime(os.path.basename(fileName), template) for
           fileName in fileNames]

    years = [dt.year for dt in dts]
    months = [dt.month for dt in dts]

    return years, months  # }}}

# vim: foldmethod=marker ai ts=4 sts=4 et sw=4 ft=python

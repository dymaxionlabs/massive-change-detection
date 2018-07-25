# Massive Change Detection - QGIS plugin

[![Build Status](https://travis-ci.org/dymaxionlabs/massive-change-detection.svg?branch=master)](https://travis-ci.org/dymaxionlabs/massive-change-detection)
[![Join the chat at https://gitter.im/dymaxionlabs/massive-change-detection](https://badges.gitter.im/dymaxionlabs/massive-change-detection.svg)](https://gitter.im/dymaxionlabs/massive-change-detection?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

QGIS 2 plugin that applies change detection algorithms on satellite imagery for
building reports for urban planning.


## Install

### Add plugins repository

To install this plugin, you need to add our QGIS Repository first.  Go to
`Plugins -> Manage and Install Plugins`.

On the Settings tab, enable `Show also experimental plugins`, and add a
repository named `Dymaxion Labs` with the following URL:

```
https://dymaxionlabs.github.io/qgis-repository/plugins.xml
```

After that, press `Reload all repositories` button to load our plugins index
into QGIS.

### Install external dependencies

This plugin makes use of some additional Python dependencies. In a terminal,
run the following:

```
pip install --user fiona numpy opencv-python rasterio shapely
```

### Install plugin

Finally, go to `Plugins -> Manage and Install Plugins`, and in `All` or `Not
Installed` tabs, search for *Massive Change Detection*.  Click `Install
plugin`.

## Usage

This is a *processing plugin*, you will have to enable the Processing Toolbox
on QGIS to use it properly.

...

### Generate change detection raster

...

### Build report of changes

...


## Development

Clone the repository inside your QGIS plugin directory.  On Ubuntu this would
be `~/.qgis2/python/plugins/`:

```
cd ~/.qgis2/python/plugins/
git clone https://github.com/dymaxionlabs/massive-change-detection
cd massive-change-detection
```

Install packages for test and code coverage.

```
pip install --user -r requirements.txt
```

If you have installed QGIS from source use `scripts/run-env-linux.sh` to set up
the environment variables so that Python can find QGIS inside your virtual
environment.  For example, if it is `/opt/qgis2`:

```
source scripts/run-env-linux.sh /opt/qgis2
```

Run tests and build code coverage reports with `make test`.

### I18n

You can find the list of supported locales is in the `LOCALES` definition on
`Makefile`. If you want to add a new language, you have to add it there first.

Prepare translations strings with `make transup`. This command will search all
translated strings in the repository and generate `.ts` files.

Edit the translations files (files ending in `.ts`) in `i18n/`.

Finally compile translation strings with `make transcompile`.


## Issue tracker

Please report any bugs and enhancement ideas using the GitHub issue tracker:

  https://github.com/dymaxionlabs/massive-change-detection/issues

Feel free to also ask questions on our [Gitter
channel](https://gitter.im/dymaxionlabs/massive-change-detection), or by email.


## Help wanted

Any help in testing, development, documentation and other tasks is highly
appreciated and useful to the project.

For more details, see the file [CONTRIBUTING.md](CONTRIBUTING.md).


## License

Source code is released under a GNU GPL v3 license.  Please refer to
[LICENSE.md](LICENSE.md) for more information.

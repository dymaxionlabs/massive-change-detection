# Massive Change Detection - QGIS plugin

QGIS 2.18+ plugin for applying change detection algorithms on high resolution
satellite imagery.


## Install

...


## Usage

...


## Development

Clone the repository inside QGIS plugin directory.  On Ubuntu this would be
`~/.qgis2/python/plugins/`:

```
cd ~/.qgis2/python/plugins/
git clone https://github.com/dymaxionlabs/massive-change-detection
cd massive-change-detection
```

Now create a virtual environment and install packages for test and code
coverage.  You will need virtualenv and pip installed.

```
virtualenv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```

Finally, use `scripts/run-env-linux.sh` to set up the environment variables so
that Python can find QGIS inside your virtual environment.

```
source scripts/run-env-linux.sh /usr
```

Run tests and build code coverage reports with `make test`.


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

Source code is released under a BSD-2 license.  Please refer to
[LICENSE.md](LICENSE.md) for more information.

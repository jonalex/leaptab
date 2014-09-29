LeapTab
=========

Tool for switching windows with leap motion.

Installation
-------------

1. Clone repository.
2. Move leap motion libraries in leap folder (`Leap.py`, `libLeap.so` and `LeapPython.so`).
3. Install `lepatab` with:

.. code-block:: bash

    python setup.py develop

Usage
-----

You can run leaptab with:

.. code-block:: bash

    leaptab

You can configure thresholds and switching window strategy:

.. code-block:: bash

    $ leaptab --help

    usage: leaptab [-h] [--use-alt-tab] [--swipe-threshold SWIPE_THRESHOLD]
                   [--toggle-interval TOGGLE_INTERVAL]

    optional arguments:
      -h, --help            show this help message and exit
      --use-alt-tab         Use alt+tab for switching windows. By default win+w
                            used.
      --swipe-threshold SWIPE_THRESHOLD
                            Threshold for swipe gestures.
      --toggle-interval TOGGLE_INTERVAL
                            Interval between open/close switch windowactions.

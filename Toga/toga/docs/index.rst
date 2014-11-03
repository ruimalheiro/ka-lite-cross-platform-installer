====
Toga
====

Toga is a Python native, OS native, cross platform GUI toolkit.

Quickstart
==========

In your virtualenv, install Toga, and then run it::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window showing the full range of widgets available
to an application using Toga.

Prerequisites
~~~~~~~~~~~~~

Toga has some minimum requirements:

* If you're on OS X, you need to be on 10.7 (Lion) or newer.

* If you're on Linux, you need to have GTK+ 3.4 or later. This is the
  version that ships with Ubuntu 12.04. If you want to use the WebView
  widget, you'll also need to have WebKit, plus the GI bindings to WebKit
  (``gir1.2-webkit-3.0``) installed.

If these requirements aren't met, Toga either won't work at all, or won't
have full functionality.

Problems with source installs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Internally, Toga is comprised of a number of subpackages - one for each
platform it supports. If you install using wheels, the install process will
correctly identify the required packages and install them. However, if you
install from source using pip, there is a `known bug in pip`_ that causes
dependencies to not be installed. It may be necessary to manually install
the following pre-requisites:

* OS X: ``pip install toga-cocoa``
* Linux: ``pip install toga-gtk toga-cassowary cassowary``
* Win32: ``pip install toga-win32 toga-cassowary cassowary``

.. _known bug in pip: https://github.com/pypa/pip/issues/1951

Problems using virtualenv under Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When on Linux, Toga uses the system native python GTK+3 bindings for display
purposes. However, if you're using a ``--no-site-packages`` virtualenv, the
Python bindings for GTK won't be in your ``PYTHONPATH``.

Unfortunately, you can't ``pip install`` GTK+ bindings, so you have to use a
workaround. To make the system GTK+ bindings available to your virtualenv,
symlinking the ``gi`` module from the system dist-packages directory into your
virtualenv's site-packages::

    $ cd $VIRTUAL_ENV/lib/python2.7/site-packages
    $ ln -si /usr/lib/python2.7/dist-packages/gi

Community
=========

Toga is part of the `BeeWare suite`_. You can talk to the community through:

 * `@pybeeware on Twitter`_

 * The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

 * The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: http://toga.readthedocs.org
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers

Contents
========

.. toctree::
   :maxdepth: 2
   :glob:

   philosophy
   tutorial/index
   reference/index
   internals/index

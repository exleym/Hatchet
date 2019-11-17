Developer Guide
===============
Operating / altering an application can be complicated, especially if there
are multiple components working together. This section of the documentation
outlines the tooling decisions made for this project and details the steps
required to make changes to the application.


Part I: Running Locally
-----------------------
The full application suite can be run on a local machine, treating each
service as a fully independent component and running them separately, while
allowing them to communicate with one-another over local HTTP.


Step 1 - Boot Hatchet API
^^^^^^^^^^^^^^^^^^^^^^^^^
Setting up the Hatchet API for local development should be fairly
straightforward. Clone the full Hatchet repo from GitHub to your local
machine.

.. note::

    Note for Windows users:

    This application was developed on Mac and Linux and has not been tested
    on Windows machines. There isn't a good reason that it shouldn't run on
    Windows, but it may take some extra tweaking and configuration.


Once the application is checked out locally and you have a project build in
your IDE of choice, you need to create a Python virtual environment to serve
as your runtime. We recommend using virtualenv and pip for package management.

.. code-block:: bash

    $ python -m virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
    (venv)$ python wsgi.py

That should be it. As long as you have a suitable python runtime (Python 3.6+)
and the dependencies installed, the basic API should "just work". Depending
on the configuration / environment selected, however, you may have varying
degrees of pre-seeded data.

The ``scripts/`` directory of the project contains several scripts to seed
additional data into the application. Scripts have been provided for the
following functionality:

* adding basic game information,
* external mappings to ESPN, CFB-Data, etc
* adding betting data
* adding TV ratings data


Step 2 - Boot Axe UI
^^^^^^^^^^^^^^^^^^^^
AxeUI is an Angular application and will require you to have Node, NPM, and
the Angular CLI installed to function properly. Let's assume those are all
already handled, and you just need to boot the application.

.. code-block:: bash

    $ cd AxeUI
    $ npm install
    $ ng serve --open

This will install all NPM dependencies and boot your Angular application on
port 4200. The ``--open`` command will cause it to load in your browser as
soon as the application is finished compiling and is served on the local dev
server.

======
README
======

:License: MPLv2
:Source: https://github.com/willkg/socorro-supersearch-test
:Issues: https://github.com/willkg/socorro-supersearch-test/issues


WHy?
====

I build this to test out supersearch queries across all supersearch fields.
Particularly how switching the Elasticsearch query type for the default
operator would affect searches with single and multiple values.


How?
====

First do::

    make .env


to copy the env template over.

Then in your ``.env`` file, set the token variables for the environments you're
going to use.

Then do::

    make build_venv


To build a Python virtual environment to run the script in.

Then run the script::

    make run


Where?
======

When you run the script, it'll prompt you for which environment to run against:
local, stage, or prod.


Who?
====

I did it. I made this script.


When?
=====

I made this at the end of June 2024.

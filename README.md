# README

License: MPLv2


# WHy?

I build this to test out supersearch queries across all supersearch fields.


# How?

First do:

```
make .env
```

to copy the env template over.

Then in your `.env` file, set the token variables for the environments you're
going to use.

Then do:

```
make build_venv
```

To build a Python virtual environment to run the script in.

Then run the script:

```
make run
```

It will prompt you for which environment to run against: local, stage, or prod.

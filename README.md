# README

License: MPLv2


# WHy?

I build this to test out supersearch queries across all supersearch fields.


# How?

First, set `CRASHSTATS_API_TOKEN` to an API token for the environment you're
testing.

Then run the script:

```
make run
```

That will build a new virtual environment and run the script in it.

To rebuild the virtual environment:

```
make build_venv
```

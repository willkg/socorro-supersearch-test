# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import os

import click
from crashstats_tools.libcrashstats import supersearch, supersearch_facet
import requests


DATE_VALUE = [">=2024-06-24", "<2024-06-25"]


def get_supersearch_fields(host):
    resp = requests.get(f"{host}api/SuperSearchFields/")
    resp.raise_for_status()
    data = resp.json()
    fields = []
    for field, val in data.items():
        if not val.get("is_exposed"):
            click.echo("Skipping {field} ...")
            continue
        if not val.get("is_returned"):
            click.echo("Skipping {field} ...")
            continue
        # FIXME(willkg): are there other reasons to skip fields?
        fields.append(field)
    return fields


def get_field_values(api_token, host, field):
    resp = supersearch_facet(
        params={
            "_facets": field,
            "date": DATE_VALUE,
        },
        host=host,
        api_token=api_token,
    )
    if field not in resp["facets"]:
        return None

    facet_data = sorted(
        resp["facets"][field], key=lambda item: item["count"], reverse=True
    )
    data = [item["term"] for item in facet_data[:3]]
    data.sort()
    return data


@click.command
@click.option(
    "--environment",
    show_default=True,
    type=click.Choice(["local", "stage", "prod"]),
    prompt=True,
)
@click.pass_context
def main(ctx, environment):
    if environment == "local":
        api_token_var = "LOCAL_API_TOKEN"
        host = "http://localhost:8000/"
    elif environment == "stage":
        api_token_var = "STAGE_API_TOKEN"
        host = "https://crash-stats.allizom.org/"
    elif environment == "prod":
        api_token_var = "PROD_API_TOKEN"
        host = "https://crash-stats.mozilla.org/"

    api_token = os.environ.get(api_token_var)
    if not api_token:
        click.echo("Need to set CRASHSTATS_API_TOKEN. Exiting.", err=True)
        ctx.exit(1)

    click.echo("---------------------------------------------------------")
    click.echo(f"Host:      {host}")
    click.echo(f"API token: {'*' * (len(api_token) - 4)}{api_token[-4:]}")
    click.echo(f"Date:      {datetime.datetime.now()}")
    click.echo("---------------------------------------------------------")

    fields = sorted(get_supersearch_fields(host=host))

    # For each field
    for field in fields:
        click.echo("\n\n\n\n\n")
        click.echo(f">>> WORKING ON {field!r} ...")

        if field == "date":
            click.echo("Skpping date ...")
            continue

        # Retrieve top 3 values
        if field == "platform":
            # We do this weird thing for platform because this is the one we're
            # trying to fix
            values = ["Mac OS X", "Windows", "Linux"]
        else:
            values = get_field_values(api_token=api_token, host=host, field=field)

        if not values:
            click.echo("no data")
            continue

        click.echo(f"{field}: {values}")

        # Do a super search for each value by itself
        for value in values:
            click.echo(f"WORKING ON {value!r}")
            try:
                supersearch_data = list(
                    supersearch(
                        params={
                            field: value,
                            "_columns": ["uuid", field],
                            "date": DATE_VALUE,
                        },
                        host=host,
                        num_results=5,
                        api_token=api_token,
                    )
                )
                for item in supersearch_data:
                    click.echo(f"* {item['uuid']}: {item[field]!r}")
            except Exception as exc:
                click.echo(f"ERROR: {exc}")

        # Do a super search for all the values at the same time
        click.echo(f"WORKING ON {values!r}")
        try:
            supersearch_data = list(
                supersearch(
                    params={
                        field: values,
                        "_columns": ["uuid", field],
                        "date": DATE_VALUE,
                    },
                    host=host,
                    num_results=5,
                    api_token=api_token,
                )
            )
            for item in supersearch_data:
                click.echo(f"* {item['uuid']}: {item[field]!r}")
        except Exception as exc:
            click.echo(f"ERROR: {exc}")


if __name__ == "__main__":
    main()

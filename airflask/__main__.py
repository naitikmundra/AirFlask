import click
import os
import sys
import shutil
import json

from airflask.deploy import run_deploy, restartapp, stopapp

def require_root():
    if os.geteuid() != 0:
        click.echo("AirFlask must be run with sudo or as root.", err=True)
        sys.exit(1)

def check_log_exists(app_path, must_exist=True):
    log_file = os.path.join(app_path, "airflask.log")
    if must_exist and not os.path.isfile(log_file):
        click.echo("Error: airflask.log not found. Did you mean to deploy the app first?", err=True)
        sys.exit(1)
    if not must_exist and os.path.isfile(log_file):
        click.echo("Error: airflask.log already exists. Did you mean to restart or stop the app?", err=True)
        sys.exit(1)
    return log_file

def validate_ssl_domain(ssl, domain):
    if ssl and not domain:
        click.echo("Error: SSL enabled but no domain specified. Use --domain to specify one.", err=True)
        sys.exit(1)

def delete_deployment_files(app_name, app_path):
    files = [
        f"/etc/systemd/system/{app_name}.service",
        f"/etc/nginx/sites-available/{app_name}",
        f"/etc/nginx/sites-enabled/{app_name}",
        os.path.join(app_path, "airflask.log")
    ]
    for file in files:
        try:
            os.remove(file)
        except Exception as e:
            click.echo(f"An error occurred while removing {file}: {e}", err=True)
            sys.exit(1)

    venv_path = os.path.join(app_path, "venv")
    try:
        shutil.rmtree(venv_path)
        click.echo(f"Deleted previous deployment: {app_path}")
    except Exception as e:
        click.echo(f"An error occurred while deleting virtual environment: {e}", err=True)
        sys.exit(1)

@click.group()
def cli():
    """FlaskAir - Deploy Flask apps in production easily. (NGINX + GUNICORN)"""
    pass

@cli.command()
@click.argument("app_path")
@click.option("--domain")
@click.option("--apptype")
@click.option("--power")
@click.option("--ssl", is_flag=True)
@click.option("--noredirect", is_flag=True)
def deploy(app_path, domain, apptype, power, ssl, noredirect):
    require_root()
    check_log_exists(app_path, must_exist=False)
    validate_ssl_domain(ssl, domain)

    try:
        run_deploy(app_path, domain, apptype, power, ssl, noredirect)
    except Exception as e:
        click.echo(f"An error occurred while deploying {app_path}. Please try redeployment!", err=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument("app_path")
@click.option("--domain")
@click.option("--apptype")
@click.option("--power")
@click.option("--ssl", is_flag=True)
@click.option("--noredirect", is_flag=True)
def redeploy(app_path, domain, apptype, power, ssl, noredirect):
    stopapp(app_path)
    require_root()
    log_file = check_log_exists(app_path)
    validate_ssl_domain(ssl, domain)

    with open(log_file, 'r') as f:
        app_name = f.read()

    delete_deployment_files(app_name, app_path)

    try:
        run_deploy(app_path, domain, apptype, power, ssl, noredirect)
    except Exception as e:
        click.echo(f"An error occurred while deploying {app_name}. Please try redeployment!", err=True)
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument("app_path")
def restart(app_path):
    require_root()
    check_log_exists(app_path)
    click.echo("Restarting app...")
    try:
        restartapp(app_path)
    except Exception:
        click.echo("An error occurred while restarting the web app.", err=True)
        sys.exit(1)
    click.echo("App restarted successfully.")

@cli.command()
@click.argument("app_path")
def stop(app_path):
    require_root()
    check_log_exists(app_path)
    click.echo("Stopping app...")
    try:
        stopapp(app_path)
    except Exception:
        click.echo("An error occurred while stopping the web app.", err=True)
        sys.exit(1)
    click.echo("App stopped successfully.")

@cli.command()
@click.argument("app_name", required=False, default=None)
@click.option("--delete", is_flag=True)
def get(app_name, delete):
    dir_path = "/var/airflask"
    file_path = os.path.join(dir_path, "airflask.txt")

    if not os.path.exists(file_path):
        click.echo("AirFlask: No web apps found!", err=True)
        sys.exit(1)

    with open(file_path, "r") as file:
        apps = json.load(file)
        
        if not app_name:
            for app in apps:
                print(f"App Name: {app[0]}, App Path: {app[1]}")
            return

        for app in apps:
            if app[0].lower() == app_name.lower():
                print(f"App Name: {app[0]}, App Path: {app[1]}")
                if delete:
                    app_path = app[1]
                    stopapp(app_path)
                    log_file = check_log_exists(app_path)
                    with open(log_file, 'r') as f:
                        real_app_name = f.read()
                    delete_deployment_files(real_app_name, app_path)
                else:
                    print("For manual modification, you can edit these files:")
                    print(f"/etc/systemd/system/{app_name}.service")
                    print(f"/etc/nginx/sites-available/{app_name}")
                    print(f"/etc/nginx/sites-enabled/{app_name}")
                return

        print("App not found.")

@cli.command()
def about():
    click.echo("AirFlask - A simple tool to deploy Flask apps in production.")
    click.echo("Created by Naitik Mundra.")
    click.echo("More info: https://github.com/naitikmundra/AirFlask")

if __name__ == "__main__":
    cli()

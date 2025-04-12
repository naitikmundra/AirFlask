import click
import os
import sys
import shutil


from airflask.deploy import run_deploy, restartapp, stopapp

@click.group()
def cli():
    """FlaskAir - Deploy Flask apps in production easily."""
    pass
@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Can be used to specify domain name for website.")
@click.option("--apptype", help="Can be used to specify web application type for optimized hosting.")
@click.option("--power", help="Can be used to specify how much traffic your server will handle.")
@click.option("--ssl", is_flag=True, help="Enable/Get SSL for the website automatically.")
@click.option("--noredirect", is_flag=True, help="Disable automatic HTTP-to-HTTPS redirection.")
def redeploy(app_path, domain, apptype, power, ssl, noredirect):
    if os.geteuid() != 0:
        print("AirFlask must be run with sudo or as root.")
        sys.exit(1)
    log_file = os.path.join(app_path, "airflask.log")

    if not os.path.isfile(log_file):
        click.echo("Error: airflask.log does not exist. Did you mean to deploy the app?", err=True)
        sys.exit(1)
    with open(log_file, 'r') as f:
        app_name = f.read()
    service_file = f"/etc/systemd/system/{app_name}.service"
    nginx_conf = f"/etc/nginx/sites-available/{app_name}"
    nginx_link = f"/etc/nginx/sites-enabled/{app_name}"
    venv_path = os.path.join(app_path, "venv")
    if ssl and not domain:
        click.echo("Error: SSL enabled but no domain specified. Use --domain to specify one.", err=True)
        sys.exit(1)
    for file in [service_file, nginx_conf, nginx_link,log_file]:
        try:
            os.remove(file)

        except Exception as e:
            click.echo(f"An error occured while redeploying {app_name}.", err=True)
            sys.exit(1)
    try:
        shutil.rmtree(venv_path)
        click.echo(f"Deleted previous deployment: {app_path}")
    
    except Exception as e:
        click.echo(f"An error occured while redeploying {app_name}.", err=True)
        sys.exit(1)
    

    run_deploy(app_path, domain, apptype, power, ssl, noredirect)
    
@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Can be used to specify domain name for website.")
@click.option("--apptype", help="Can be used to specify web application type for optimized hosting.")
@click.option("--power", help="Can be used to specify how much traffic your server will handle.")
@click.option("--ssl", is_flag=True, help="Enable/Get SSL for the website automatically.")
@click.option("--noredirect", is_flag=True, help="Disable automatic HTTP-to-HTTPS redirection.")
def deploy(app_path, domain, apptype, power, ssl, noredirect):
    if os.geteuid() != 0:
        print("AirFlask must be run with sudo or as root.")
        sys.exit(1)
    log_file = os.path.join(app_path, "airflask.log")

    if os.path.isfile(log_file):
        click.echo("Error: airflask.log already exists. Did you mean to restart or stop the app?", err=True)
        sys.exit(1)

    if ssl and not domain:
        click.echo("Error: SSL enabled but no domain specified. Use --domain to specify one.", err=True)
        sys.exit(1)

    run_deploy(app_path, domain, apptype, power, ssl, noredirect)

@cli.command()
@click.argument("app_path")
def restart(app_path):
    if os.geteuid() != 0:
        print("AirFlask must be run with sudo or as root.")
        sys.exit(1)
    log_file = os.path.join(app_path, "airflask.log")

    if not os.path.isfile(log_file):
        click.echo("Error: airflask.log not found. Did you mean to deploy the app first?", err=True)
        sys.exit(1)

    click.echo("Restarting app...")
    restartapp(app_path)
    click.echo("App restarted successfully.")

@cli.command()
@click.argument("app_path")
def stop(app_path):
    if os.geteuid() != 0:
        print("AirFlask must be run with sudo or as root.")
        sys.exit(1)
    log_file = os.path.join(app_path, "airflask.log")

    if not os.path.isfile(log_file):
        click.echo("Error: airflask.log not found. Did you mean to deploy the app first?", err=True)
        sys.exit(1)

    click.echo("Stopping app...")
    stopapp(app_path)
    click.echo("App stopped successfully.")

@cli.command()
def about():
    """Show information about FlaskAir."""
    click.echo("AirFlask - A simple tool to deploy Flask apps in production.")
    click.echo("Created by Naitik Mundra.")
    click.echo("More info: https://github.com/naitikmundra/AirFlask")

if __name__ == "__main__":
    cli()

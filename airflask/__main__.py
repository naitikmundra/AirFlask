import click
from airflask.deploy import run_deploy, restart, stop

@click.group()
def cli():
    """FlaskAir"""
    pass

@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Domain name for the Flask app")
@click.option("--ssl", is_flag=True, help="Setup ssl for website automatically.")
@click.option("--noredirect", is_flag=True, help="Don't redirect all http requests to https.")

def deploy(app_path, domain, ssl, noredirect):
    log_file = os.path.join(app_path, "airflask.log")
    if os.path.isfile(log_file):
        print("airflask.log already present. Did you mean to restart or stop the app?")
    else:
        if ssl: 
            if not domain:
                print("Domain not specified, either remove ssl flag or specify a domain with --domain")
                return None
        run_deploy(app_path, domain,ssl,noredirect)
        
        
@cli.command()
@click.argument("app_path")
def restart(app_path):
    log_file = os.path.join(app_path, "airflask.log")
    if os.path.isfile(log_file):
        print("airflask.log not present. Did you mean to deploy the app?")
    else:
        restart(app_path)
    
@cli.command()
@click.argument("app_path")
def stop(app_path):
    log_file = os.path.join(app_path, "airflask.log")
    if not os.path.isfile(log_file):
        print("airflask.log not present. Did you mean to deploy the app?")
    else:
        stop(app_path)
        
@cli.command()
def about():
    print("Airflask is a Python library created by Naitik Mundra, designed to deploy Flask apps in production with just a few lines of code! Learn more about Airflask at https://github.com/naitikmundra/AirFlask")
if __name__ == "__main__":
    cli()


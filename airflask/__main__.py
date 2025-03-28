import click
from airflask.deploy import run_deploy, restart, stop

@click.group()
def cli():
    """FlaskAir"""
    pass

@cli.command()
@click.argument("app_path")
@click.option("--domain", help="Domain name for the Flask app")
@click.option("--db", is_flag=True, help="Set up MySQL for the app")
def deploy(app_path, domain, db):
    log_file = os.path.join(app_path, "airflask.log")
    if os.path.isfile(log_file):
        print("airflask.log already present. Did you mean to restart or stop the app?")
    else:
        run_deploy(app_path)
        app_path
        
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
        
if __name__ == "__main__":
    cli()


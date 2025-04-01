import os
import subprocess
import getpass  
import re
import multiprocessing

def optimal_workers():
    cores = multiprocessing.cpu_count()
    return 2 * cores + 1
def get_private_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "An error occured while fetching ip address."
def get_public_ip():
    try:
        return subprocess.check_output(["curl", "-s", "https://checkip.amazonaws.com"]).decode().strip()
    except Exception:
        return get_private_ip()
        
def stop(app_path):
    log_file = os.path.join(app_path, "airflask.log")
    with open(log_file, 'r') as file:
        appname = file.read()
    subprocess.run(["sudo", "systemctl", "stop", appname])
    
    subprocess.run(["sudo", "systemctl", "stop", "nginx"])
    
def restart(app_path):
    log_file = os.path.join(app_path, "airflask.log")
    with open(log_file, 'r') as file:
        appname = file.read()
    subprocess.run(["sudo", "systemctl", "restart", appname])
    
    subprocess.run(["sudo", "systemctl", "restart", "nginx"])

def run_deploy(app_path, domain,ssl,noredirect):
    
    if not domain: 
        ssl = None
        domain = "_"
    nginx_default = "/etc/nginx/sites-enabled/default"
    if os.path.exists(nginx_default):
        subprocess.run(["sudo", "rm", nginx_default])
    app_name = os.path.basename(os.path.abspath(app_path))
    service_file = f"/etc/systemd/system/{app_name}.service"
    nginx_conf = f"/etc/nginx/sites-available/{app_name}"
    nginx_link = f"/etc/nginx/sites-enabled/{app_name}"
    
    print(f"📦 Deploying {app_name}...")

    print("🔧 Installing dependencies...")
    subprocess.run(["sudo", "apt", "update"])
    subprocess.run(["sudo", "apt", "install", "-y", "python3-venv", "python3-pip", "nginx"])

    venv_path = os.path.join(app_path, "venv")
    print("🐍 Creating virtual environment...")
    subprocess.run(["python3", "-m", "venv", venv_path])
    
    print("📦 Installing Flask and Gunicorn...")
    subprocess.run([f"{venv_path}/bin/pip", "install", "flask", "gunicorn"], cwd=app_path)

    wsgi_path = os.path.join(app_path, "wsgi.py")
    if not os.path.exists(wsgi_path):
        print("📝 Creating wsgi.py...")
        with open(wsgi_path, "w") as f:
            f.write(f"from app import app\n\nif __name__ == '__main__':\n    app.run()")
    username = getpass.getuser()
    workers = str(optimal_workers())
    print(f"Total workers: {workers}")
    service_config = f"""[Unit]
    Description=Gunicorn instance to serve {app_name}
    After=network.target

    [Service]
    User={username}
    Group=www-data
    WorkingDirectory={app_path}
    ExecStart={venv_path}/bin/gunicorn --workers {workers} --bind unix:{app_path}/{app_name}.sock wsgi:app

    [Install]
    WantedBy=multi-user.target
    """

    nginx_conf = "/etc/nginx/nginx.conf"
    username = "username"  

    with open(nginx_conf, "r") as file:
        config = file.read()

    updated_config = re.sub(r"user\s+\S+;", f"user {username};", config)

    with open(nginx_conf, "w") as file:
        file.write(updated_config)

    print(f"Username updated in nginx.conf to {username}")
    with open('airflask.log','w') as file:
        file.write(app_name)
    with open("service_file.tmp", "w") as f:
        f.write(service_config)
    subprocess.run(["sudo", "mv", "service_file.tmp", service_file])
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "start", app_name])
    subprocess.run(["sudo", "systemctl", "enable", app_name])

    nginx_config = f"""server {{
    listen 80;
    server_name {domain};

    location / {{
        include proxy_params;
        proxy_pass http://unix:{app_path}/{app_name}.sock;
        }}
    }}"""
    with open("nginx_conf.tmp", "w") as f:
        f.write(nginx_config)
    subprocess.run(["sudo", "mv", "nginx_conf.tmp", nginx_conf])
    subprocess.run(["sudo", "ln", "-s", nginx_conf, nginx_link])
    if ssl:
        print("Getting an ssl certificate for you")
        subprocess.run(["sudo", "apt", "install", "certbot", "python3-certbot-nginx"])
        if noredirect:
            subprocess.run(["sudo", "certbot", "--nginx", "--no-redirect"])
        else:
            subprocess.run(["sudo", "certbot", "--nginx", "--redirect"])
        subprocess.run(["sudo", "bash", "-c", 'echo "0 0,12 * * * certbot renew --quiet && systemctl reload nginx" | crontab -'])

    subprocess.run(["sudo", "systemctl", "restart", "nginx"])

    ip_address = get_public_ip()
    print(f"✅ Deployment completed! App with name '{app_name}' is live at: http://{domain}")
    if ssl:
        print(f"Also live at: https://{domain}")

# AirFlask

<p align="center">
  <img src="https://github.com/user-attachments/assets/73f561cb-74aa-428e-be29-08694574dc2e" width="250" height="250">
</p>

Simplest way to host flask web apps in production - Using nginx and gunicorn.

## Installation
```
pip install airflask
```

## Features
- 🚀 One line production deployment for flask apps. 
- 🔧 Installs all dependencies, and manages everything. 
- ⚡ Powered by a nginx + gunicorn server.
- 🤖 Auto-tunes the best hosting config based on your server specs.


## Usage
**Deploying**: A single line that manages everything and your app goes live with no hassle!

```
sudo airflask deploy <path>
```
- >where `<path>` is the full path to the parent folder containing your app.py
- >Be sure to rename your main flask file to `app.py`
- >App will be hosted on localhost, your private and public ip address (if static and unshared).
- >for eg. `sudo airflask deploy /home/naitik/flaskecomapp/`

## Deploying with Domain and SSL (Free SSL via Let's Encrypt)

```
sudo airflask deploy <path> --domain <example.com>
```

```
sudo airflask deploy <path> --domain <example.com> --ssl --noredirect

```

## App Type and Power

```
sudo airflask deploy <path> --apptype <app_type> 
```

```
sudo airflask deploy <path> --power <high/low/med>
```

More instructions and details at https://github.com/naitikmundra/airflask


## Stop or Restart
```
sudo airflask restart <path>
sudo airflask stop <path>
```
Restart your app after you make changes.

## Contact
- Feel free to email me at  naitikmundra18@gmail.com for any queries or suggestions.
- Or DM me on instagram: https://instagram.com/naitikmundra






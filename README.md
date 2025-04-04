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



## Usage
**Deploying**: Just run this single line — it auto-installs all dependencies and your app goes live!

```
sudo airflask deploy <path>
```
- where `<path>` is the full path to the parent folder containing your app.py
- App will be hosted on localhost, your private and public ip address (if static and unshared).
- for eg. `sudo airflask deploy /home/naitik/flaskecomapp/`

## Deploying with Domain and SSL (Free SSL via Let's Encrypt)

```
sudo airflask deploy <path> --domain <example.com>
```

```
sudo airflask deploy <path> --domain <example.com> --ssl --noredirect
```

## Note
- Be sure to rename your main flask file to `app.py`
- Make sure your domain points to your ip address for functionality.
- `--ssl` will not work without a domain specified.
- by default if `--ssl` is specified all http requests will be redirected to https unless `--noredirect` is used.

## Specifying App Type
It is important to know which kind of web app you are trying to deploy for efficient hosting.

```
sudo airflask deploy <path> --domain <example.com> --type <app_type>
```
App type can be:
- `chatapp ` : web apps which use websockets (*other app types may cause web socket functionality to not work properly)
- `cpubound` : web apps which are heavily cpu dependent (AI/ML, other cpu focused work)

By *default* hosting is optimized for i/o bound websites (which are heavily DB, API and file management oriantated like `ecommerce`, `blog`, etc)


## Stop or Restart
```
sudo airflask restart <path>
sudo airflask stop <path>
```
Restart your app after you make changes.

## Contact
- Feel free to email me at  naitikmundra18@gmail.com for any queries or suggestions.
- Or DM me on instagram: https://instagram.com/naitikmundra






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

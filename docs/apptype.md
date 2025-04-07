## Specifying App Type
It is optional yet important to know which kind of web app you are trying to deploy for efficient hosting.

```
sudo airflask deploy <path> --domain <example.com> --type <app_type>
```
App type can be:
- `chatapp ` : web apps which use websockets (*other app types may cause web socket functionality to not work properly)
- `cpubound` : web apps which are heavily cpu dependent (AI/ML, other cpu focused work)

By *default* hosting is optimized for i/o bound websites (which are heavily DB, API and file management oriantated like `ecommerce`, `blog`, etc), no need to specify apptype .

### Specifying App Power

```
sudo airflask deploy <path> --power <high/low/med>
```
Based on the amount of traffic your app recieves you can decide if you want:
- >100> Active users - `low` power would be good for small servers.
- >1K> Active users - `med` power would be good for medium servers.
- >1K+ Active users - `high` power would be good for big servers.


# Power Details
- `low` power means app will be using `4 threads` OR `2000 connections` and `2 workers`. (limiting no. of workers here)
- `med` power means app will be using `8 threads` OR `2000 connections` and `x workers`. (workers based on cpu cores)
- `high` power means app will be using `16 threads` OR `4000 connections` and `x workers`. (workers based on cpu cores)

`Note` - In genral worker number will be no. of cpu cores in system multiplied by 2 plus 1. A server with 2 cores will have 5 workers.

# WHAT?
Gunicorn `workers` are individual Python processes that handle incoming web requests. They are the core components that execute your application code. 



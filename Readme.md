# Server
# Run 一個
## Auth_Server
IP：0.0.0.0

Port：5000
```
$ python Auth_Server.py
```

## RESTful_server
IP：0.0.0.0

Port：5001
```
$ python RESTful_Server.py
```

# Run 多個
## Auth_Server
```
gunicorn -c gun_a.py Auth_Server:app
```

## RESTful_server
```
gunicorn -c gun_r.py RESTful_Server:app
```

# PostgreSQL
user：```postgres```

password：```123456```

host：```127.0.0.1```

port：```5432```




# Work
JWT 驗證(登路、登出、註冊)

GET /api/v1/resources/users/information

POST /api/v1/action/send-request

PUT /api/v1/resources/users/information

GET /api/v1/resources/users/trackers 

POST /api/v1/resources/users/addtracker 

POST /api/v1/resources/users/deltracker 

# Skip
GET /api/v1/resources/users/location

PUT /api/v1/resources/users/boundary

GET /api/v1/resources/users/responses
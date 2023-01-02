![Logo of the project](logo.webp)

# HEROES 3 REST API

API for heroes 3 of might and magic. Based on django and scrapy frameworks. On start it parse https://heroes.thelazy.net/ and fill the database with data. 

## Installing / Getting started

```shell
git clone https://github.com/volodymyr-vereshchak/heroes3-rest-api
cd heroes3-rest-api
initilize enviroment variables .env
docker-compose up --build
```
This project use dropbox API for store image files. So u need to create account and application to initilize next enviroment variables
```shell
DROPBOX_OAUTH2_TOKEN = DROPBOX_OAUTH2_TOKEN
DROPBOX_APP_KEY = DROPBOX_APP_KEYb
DROPBOX_APP_SECRET = DROPBOX_APP_SECRET
DROPBOX_OAUTH2_REFRESH_TOKEN = DROPBOX_OAUTH2_REFRESH_TOKEN
DROPBOX_ROOT_PATH = DROPBOX_ROOT_PATH
```
## Links

You can test api on the next links:

- Heroes API: https://heroes-3-api.onrender.com/api/heroes/
- User API: https://heroes-3-api.onrender.com/api/user/register (/token/refresh)
- Swagger: https://heroes-3-api.onrender.com/api/schema/swagger-ui/
- Redoc: https://heroes-3-api.onrender.com/api/schema/redoc/

Example of [Starlette](https://www.starlette.io/) accommodation rental application made with [Piccolo ORM](https://www.piccolo-orm.com/) and [Piccolo Admin](https://github.com/piccolo-orm/piccolo_admin).

Open terminal and run:

```shell
virtualenv -p python3 envname
cd envname
source bin/activate
git clone https://github.com/sinisaos/starlette-piccolo-rental.git
cd starlette-piccolo-rental
pip install -r requirements.txt
sudo -i -u yourpostgresusername psql
CREATE DATABASE ads;
\q
touch .env
## for upload via Dropzone make upload folder in static
## mkdir static/uploads

## put this in .env file
## DB_NAME="your db name"
## DB_USER="your db username"
## DB_PASSWORD="your db password"
## DB_HOST="your db host"
## DB_PORT=5432
## SECRET_KEY="your secret key"
## for Cloudinary uploads
## CLOUDINARY_API_KEY="your_api_key"
## CLOUDINARY_API_SECRET="your_api_secrets"

## runing migrations for admin
piccolo migrations forwards user
piccolo migrations forwards session_auth
## runing migrations for site
piccolo migrations forwards ads
## create admin user
piccolo user create
uvicorn app:app --port 8000 --host 0.0.0.0 
```
Two options for upload images:
1. DropzoneJS for upload images to filesystem
2. Upload images to [Cloudinary](https://cloudinary.com/) because Heroku filesystem is not suitable for file upload.  
   More info on link https://help.heroku.com/K1PPS2WM/why-are-my-file-uploads-missing-deleted. To upload images to Cloudinary sign up to [Cloudinary](https://cloudinary.com/) free account, set CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET to .env file, comment UPLOAD_FOLDER in settings.py, then uncomment Cloudinary and comment Dropzone in endpoints and templates and everything shoud be fine. 

After site is running log in as admin user and add ads, reviews etc. For non admin user you can sign up and post content.

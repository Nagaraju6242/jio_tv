# Django Server to watch live Jio TV

## Installation
clone the repo
```
git clone https://github.com/Nagaraju6242/jio_tv.git
```

## Install requirements
```
pip install -r requirements.txt
```



## Login 
Open the browser and go to http://jiologin.unaux.com/
Enter your Jio ID and Password
Click on Login
Paste the credentials in a file named creds.json in the same directory as `settings.py` file

## Run the server
```
python manage.py runserver
```

Go to http://127.0.0.1:8000/ and select the channel you want to watch
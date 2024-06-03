# Installation steps 
<br>
Please note that you need to make a file called '.env' and this file should have environments variables as the ones listed in .env.example
<br>
<br>

## After this you will need to open docker in your windows and 

```
docker-compose up --build -d
```

## if you don't have docker please run the following commands in shell

```
python manage.py wait_for_db
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 --noreload
```

## After this please head to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) 

You will get every endpoint documented, please note due to the lack of time there could be improvements in the code 

Thanks again!
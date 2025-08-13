# Requirements 

- install docker desktop for windows

# Commands

- change the .env.prod based on your environment variables
- change the docker-compose file for the port you want to access the app (default 8001)
- run "- docker-compose -f docker-compose-.yml run --rm src sh -c "python manage.py createsuperuser"" to create super user to access admin
- run "docker-compose -f docker-compose.yml build" to build the project
- run "docker-compose -f docker-compose.yml up" and  open the project in localhost:8001

# URL
- http://localhost:8001/api/docs/ for endpoint documentation
- http://localhost:8001/aadmin for admin page (dont forget to create a superuser)
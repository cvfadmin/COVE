# COVE
Computer Vision Exchange for Data, Annotation and Tools

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
PostgreSQL

Virtualenv


### Installing

1. Get your PostgreSQL server running. (Default port is 5432)
2. Create a empty database. (Called cove in following example)
3. Set up a virtual machine and run backend server using following commands:
   ```
   3.1 cd backend/
   
   3.2 virtualenv venv/
   
   3.3 source venv/bin/activate (starting the virtual machine)
   
   3.4 pip install -r requirements.txt (installing required packages)
   
   3.5 config your database settings in backend/application/\_\_init\_\_.py
   
   (line 16  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://username:password@localhost:port_number/database_name")
   
   3.6 python db_create.py (create database according to your models)
   
   3.7 python application.py (get the server running)
   ```
   You can skip step 3.4~3.6 once you get your database set up at the first time.
4. Deploy your frontend locally using the following commands:
   * 4.1 cd frontend/
   * 4.2 python -m SimpleHTTPServer 8000 (8000 refer to the portnumber)
5. Check the website at http://localhost:8000/

### Reminds:
You can check your environment configurations at backend/application/__init__.py and frontend/js/cove.js to make sure the frontend can sent request to backend at the right port.


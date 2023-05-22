# CMPE-321-Project-3

## Requirements
* MySQL
* Python(>3.8) and pip module.

## Setup
If you have the requirements;

1. Install the required packages by running the following command:

       pip install -r requirements.txt

2. (Optional) Set up a virtual environment to prevent conflicts. You can learn more about virtual environments [here](https://docs.python.org/3/library/venv.html#module-venv).

3. Create a virtual environment:
   ```
   python3 -m venv env
   ```
4. Activate the virtual environment:
  * For macos/linux:
  ```
  source env/bin/activate
  ```
  * For windows (command prompt):
  You may also need to execute following command if you get an error: ``` Set-ExecutionPolicy Unrestricted -Scope Process ```
   ```
  .\env\Scripts\activate.bat or env\Scripts\activate
  ```
  * For Windows (Git Bash):
   ```
   source env/Scripts/activate
   ```
    
5. Install the required packages: 
```
pip install -r requirements.txt
```

## Deployment

1. Create a config.py file where you initialized the project and insert the following configuration:
```
class Config:
    HOST="127.0.0.1"
    USER=<YOUR_USERNAME>
    PASSWORD=<YOUR_PASSWORD>
    DATABASE=<YOUR_DB_NAME>
    API_KEY=<YOUR_API_KEY>
```
2.  Create the database, for this do the following:
```
cd App
python create_db.py
```
Ensure that your MySQL database server is up and running, it should write: ```Triggers are executed```.

3. Set the Flask application environment variable:

* For MacOs/Linux:
```
export FLASK_APP=/app.py
```
* For windows:
```
set FLASK_APP=/app.py
```

4. Run the Flask application:
```
flask run
```
5. Access the application in your web browser at [http://localhost:5000](http://127.0.0.1:5000/login/). It will redirect you to login page.



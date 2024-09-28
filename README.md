
# Health_Record_System

A detailed proposal on the topic of saving files (in this proposal, health records) on the IPFS distributed network

Here the admin manages necessary relationships between a doctor and a patient and files which have been uploaded; then the users receive their mail Id after registration from the administration.

![alt text](https://github.com/charan-manigandan/Health_Record_System/blob/main/img.jpg?raw=true)


## Run Locally

Clone the project

```bash
  git clone https://github.com/charan-manigandan/Health_Record_System.git
```

Go to the project directory

```bash
  cd secured_health_record_system
```

Install dependencies

```bash
  pip install -r requirements.txt
```
make sure you migrate to db

```bash
  python manage.py makemigrations
```

```bash
  python manage.py migrate
```

Start the server 

```bash
  python manage.py runserver
```

## Diagram

![alt text](https://github.com/charan-manigandan/Health_Record_System/blob/main/repr.jpg?raw=true)


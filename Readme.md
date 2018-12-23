#### timereport_backend

#### Requirements

- For development you'll require a local Docker
- Chalice

#### Instructions

- make run

```
Will pull and run amazon/dynamodb-local from docker on port 8000
Make sure to run chalice as well.


# In Production:

Point os.environ['DB_URL'] to your production amazonaws database.

Chalice will create data there as well as fetch data from it.


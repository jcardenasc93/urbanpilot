# Urban Pilot

## Requirements
- `python 3.8 or greater`
- `Flask 2.0.1`
- `PostgreSQL 12 or greater`
- `Celery 5.1`

## Run in local environment
Please follow the next steps to run the Flask API in your local machine:
1. Clone the repo
2. Copy `.env.example` to `.env` file and adjust the value for the environment variables 
3. Install `pipenv` if not installed (`pip install pipenv`)
4. In the root of the project run `pipenv install` and then `pipenv shell`
5. Run `python run.py` and your server should be alive on `localhost:8008`

## Endpoints
### Customer
#### Create customer

`POST /customer`. Use the folowing JSON body

```json
{
    "first_name": "Jhon",
    "last_name": "Doe",
    "middle_name": "Paul [Optional]",
    "email": "jhon.doe@example.com",
    "zipcode": 94118
}
```

**NOTE:** Don't forget to include the header `Content-Type: application/json`

#### Retrieve customers info

`GET /customer`, `GET /customer/<customer_id>`

### Locations Rank

`GET /locations/rank`

### Server status

`GET /alive`

## Custom Flask CLI commands

### Analytics

In order to get most common locations rank just run `flask analytics rank_zipcodes --top <number>`

### GIS

To calculate the distance between two zipcodes run `flask gis calc_distance  <zipcode1> <zipcode2>`

## Additional Notes

This project is deployed on [Heroku](https://launch-urbanpilot.herokuapp.com/)

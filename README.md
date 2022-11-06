# FetchRewards-backend-takehome
FetchRewards Backend Engineering take-home assignment

### [Design Doc](./design-doc.md)

# Running the project

### If python >= 3.7 is installed locally
1. cd into the project root (where the make file is)
2. Build the package using `make package`, this will install the required python packages
3. Run the unittests using `make test`
4. Start the app using `make app`
5. This should start the HTTP server on port 8001
6. Go to [Docs](http://localhost:8001/docs)
7. This opens Swagger docs, where we can trigger the endpoints using the UI

### If python is not installed locally, below is the docker solution
1. Make sure docker daemon is started and running
2. Run `make docker`, this will build a image and spinup the container
3. Go to [Docs](http://localhost:8001/docs)
4. This opens Swagger docs, where we can trigger the endpoints using the UI

# Testing

Testing Payload for the `add` transaction
```
[
    {
        "payer": "DANNON",
        "points": 300,
        "timestamp": "2022-10-31T10:00:00Z"
    },
    {
        "payer": "UNILEVER",
        "points": 200,
        "timestamp": "2022-10-31T11:00:00Z"
    },
    {
        "payer": "DANNON",
        "points": -200,
        "timestamp": "2022-10-31T15:00:00Z"
    },
    {
        "payer": "MILLER COORS",
        "points": 10000,
        "timestamp": "2022-11-01T14:00:00Z"
    },
    {
        "payer": "DANNON",
        "points": 1000,
        "timestamp": "2022-11-02T14:00:00Z"
    }
]
```
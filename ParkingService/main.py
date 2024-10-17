import uvicorn
from fastapi import FastAPI

import repository
from api import accountAPI, paymentAPI, parkingPlaceAPI, parkedCarAPI

app = FastAPI()

app.include_router(accountAPI.router)
app.include_router(paymentAPI.router)
app.include_router(parkingPlaceAPI.router)
app.include_router(parkedCarAPI.router)


if __name__ == "__main__":
    repository.create_data_to_populate_parkingPlaces_and_parkedCar_tables()
    repository.create_data_to_populate_payment_table()

    uvicorn.run(app, host="0.0.0.0", port=8000)

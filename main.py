
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import io

app = FastAPI()

@app.post("/api/assign")
async def assign_trips(trips: UploadFile = File(...), drivers: UploadFile = File(...)):
    try:
        trips_df = pd.read_csv(io.StringIO((await trips.read()).decode("utf-8")))
        drivers_df = pd.read_csv(io.StringIO((await drivers.read()).decode("utf-8")))

        assignments = []
        for _, trip in trips_df.iterrows():
            available = drivers_df[
                (drivers_df['VehicleType'] == trip['VehicleType']) &
                (drivers_df['Zone'] == trip['Zone'])
            ]
            if not available.empty:
                driver = available.iloc[0]
                assignments.append(f"Trip {trip['TripID']} → Driver {driver['DriverID']}")
            else:
                assignments.append(f"Trip {trip['TripID']} → No match found")

        return JSONResponse(content={"output": "\n".join(assignments)})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




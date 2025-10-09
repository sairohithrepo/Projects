from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Sensor(BaseModel):
    temp: int
    pressure: int

class Usensor(BaseModel):
    temp: Optional[int] = None
    pressure: Optional[int] = None

# Dictionary to store sensor data
sensors_data = {
    1: {"temp": 15, "pressure": 16}
}

@app.get("/get-sensor_data/{sensor_id}")
def get_sensor_data(sensor_id: int):
    return sensors_data.get(sensor_id, {"error": "Sensor not found"})

@app.get("/get_by_temp")
def get_sensor_by_temp(temp: int):
    for sensor_id, sensor in sensors_data.items():
        if sensor["temp"] == temp:
            return sensor
    return {"data": "not found"}

@app.post("/create-sensor/{sensor_id}")
def create_sensor(sensor_id: int, sensor: Sensor):
    if sensor_id in sensors_data:
        return {"error": "sensor exists"}
    sensors_data[sensor_id] = sensor.dict()
    return sensors_data[sensor_id]

@app.put("/update_sensor/{sensor_id}")
def update_sensor(sensor_id: int, sensor: Usensor):
    if sensor_id not in sensors_data:
        return {"error": "sensor does not exist"}
    
    stored_sensor = sensors_data[sensor_id]

    if sensor.temp is not None:
        stored_sensor["temp"] = sensor.temp
    if sensor.pressure is not None:
        stored_sensor["pressure"] = sensor.pressure

    sensors_data[sensor_id] = stored_sensor
    return sensors_data[sensor_id]

@app.delete("/deletesensor/{sensor_id}")
def delete_sensor(sensor_id: int):
    if sensor_id not in sensors_data:
        return {"error": "sensor id does not exist"}
    
    del sensors_data[sensor_id]
    return {"message": f"Sensor {sensor_id} deleted successfully"}

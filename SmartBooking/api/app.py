from fastapi import FastAPI

app = FastAPI(title="SmartBooking API")


@app.get("/health")
def health():
    return {"message": "All good API is running"}

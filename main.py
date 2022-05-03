from fastapi import FastAPI
#app contiene toda la aplicacion como una instancia de FasAPI
app = FastAPI()

@app.get("/")
def home():
    return {"hello":"world"}


#python
from typing import Optional

#Pydantic
from pydantic import BaseModel
#Pydantic
from fastapi import FastAPI
from fastapi import Body

#app contiene toda la aplicacion como una instancia de FasAPI

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] =None
    is_married: Optional[bool] = None
    



@app.get("/")
def home():
    return {"hello":"world"}

 #Reques and Response body
 #Body(...) nos indica que el parametro que enviamos es obligatorio
@app.post("/person/new")
def create_person(person: Person  = Body(...)):
     return person
 

#python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field
#Pydantic
from fastapi import FastAPI, Path, Query,Body
#app contiene toda la aplicacion como una instancia de FasAPI

app = FastAPI()

class HairColor(Enum):
    white="White"
    brown="brown"
    black="Black"
    blonde="Blonde"
    red="Red"
    
    
    
#Models
class Person(BaseModel):
    first_name: str = Field(...,min_lenght = 1,max_lengt=50,example="Luca")
    last_name: str  = Field(...,min_lenght = 1,max_lengt=50,example="Manea")
    age: int = Field(...,gt=0,le = 115,example=28)
    hair_color: Optional[HairColor] =Field(default =None, exaple="black")
    is_married: Optional[bool] = Field(default = None,example=False)
#    class Config:
#        schema_extra = {
#            "Luca":{
#                "first_name":"Luca",
#                "last_name":"Manea",
#                "age":28,
#                "hair_color":"brown",
#                "is_married": False
#            }
#        }    


class Location(BaseModel):
    city: str
    state :str
    country: str






@app.get("/")
def home():
    return {"hello":"world"}

 #Reques and Response body
 #Body(...) nos indica que el parametro que enviamos es obligatorio
@app.post("/person/new")
def create_person(person: Person  = Body(...)):
     return person
 
 
#Valiciones: QueryParameters

@app.get("/person/detail")
def show_person(name:Optional[str] = Query(None,min_length=1,max_length= 50,
                title="Person Name", description="This is the persona name. Its between 1 and 50 characters"),
                age: str = Query(..., title="Person Age",
                                 description="This is the person age its Required")):
    return {name:age}

#validaciones: Path paramaeters

@app.get("/person/detail/{person_id}")
def show_person(person_id:int = Path(..., gt=0, title= "Person Id",
                    description= "This is the Person Id its Required")):
    return {person_id:"It Exist!"}
 
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(...,
                          title="Person Id",
                          description="This is the person id",
                          gt=0),
        person:Person = Body(...),
        location: Location = Body(...)
        ):
    results = person.dict()
    results.update(location.dict())
    return results
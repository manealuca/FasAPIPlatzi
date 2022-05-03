#python
from typing import Optional

#Pydantic
from pydantic import BaseModel
#Pydantic
from fastapi import FastAPI, Path, Query,Body
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
 

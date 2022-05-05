#python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field, EmailStr
#Pydantic
from fastapi import FastAPI, Form, Header, Path, Query,Body, UploadFile, status,Cookie, File, HTTPException

#app contiene toda la aplicacion como una instancia de FasAPI
app = FastAPI()

class HairColor(Enum):
    white="White"
    brown="brown"
    black="Black"
    blonde="Blonde"
    red="Red"
    
    
    
#Models
class PersonBase(BaseModel):
    first_name: str = Field(...,min_lenght = 1,max_lengt=50,example="Luca")
    last_name: str  = Field(...,min_lenght = 1,max_lengt=50,example="Manea")
    age: int = Field(...,gt=0,le = 115,example=28)
    hair_color: Optional[HairColor] =Field(default =None, exaple="black")
    is_married: Optional[bool] = Field(default = None,example=False)
    password:str= Field(...,min_length=8,max_length=50)
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

#class Person(PersonBase):
#    


class Location(BaseModel):
    city: str
    state :str
    country: str




class LoginOut(BaseModel):
    username: str = Field(...,max_length=25,example="lala1234656")
    message:str =Field(default="login succesufll")




@app.get(path="/",status_code=status.HTTP_200_OK)
def home():
    return {"hello":"world"}

 #Reques and Response body
 #Body(...) nos indica que el parametro que enviamos es obligatorio
@app.post(path="/person/new",response_model=PersonBase,response_model_exclude='password',status_code=status.HTTP_201_CREATED)
def create_person(person: PersonBase  = Body(...)):
     return person
 
 
#Valiciones: QueryParameters

@app.get(path="/person/detail",status_code=status.HTTP_200_OK)
def show_person(name:Optional[str] = Query(None,min_length=1,max_length= 50,
                title="Person Name", description="This is the persona name. Its between 1 and 50 characters"),
                example="Christian",
                age: str = Query(..., title="Person Age",
                                 description="This is the person age its Required",
                                 example=1)):
    return {name:age}

#validaciones: Path paramaeters
persons = [1,2,3,4,5]
@app.get("/person/detail/{person_id}")
def show_person(person_id:int = Path(..., gt=0, title= "Person Id",
                    description= "This is the Person Id its Required",
                    example=110)):
    if person_id not in persons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This person doesnt exist!")
    return {person_id:"It Exist!"}
 
 
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(...,
                          title="Person Id",
                          description="This is the person id",
                          gt=0,example=112),
        person:PersonBase = Body(...),
        location: Location = Body(...)
        ):
    results = person.dict()
    results.update(location.dict())
    return results

#Forms
@app.post(path="/login", response_model=LoginOut,
          status_code=status.HTTP_200_OK)
def login(username:str = Form(...),password: str =Form(...)):
    return LoginOut(username=username)



#Cookies and headers parameters
@app.post(path="/contact",status_code=status.HTTP_200_OK)
def contact(first_name:str = Form(...,max_length=25,min_length=1),
            last_name: str =Form(...,max_length=25,min_length=1),
            email:str =EmailStr(...),
            mmessage:str = Form(...,min_length=50,max_length=255),
            user_agent: Optional[str] =Header(default=None),
            ads: Optional[str]= Cookie(default = None)):
    return user_agent


#Files

@app.post(path="/post-iamge")
#si importamos list desde el modulo typing podriamos cargar varias imagenes al mismo timepo
# def post_image(images: List[UploadFile] = File(...)):
#   pass
def post_image(image:UploadFile = File(...)):
    return{
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024,ndigits=2)
    }


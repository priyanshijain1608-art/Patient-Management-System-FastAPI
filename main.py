from fastapi import FastAPI , Path , HTTPException , Query
from pydantic import BaseModel,Field,computed_field,Field
import json
from typing import Annotated,Optional
from fastapi.responses import JSONResponse

app=FastAPI()

#app created

#now let's create api's

@app.get("/")
def greet():
    return {"message":"PATIENT MANAGEMENT SYSTEM"}

@app.get('/about')
def about():
    return {"message":"This is a Fully functioned patient management system powered by - API"}


def load_data(): #retrieval data from json
    with open("patients.json") as f:
        data=json.load(f)
    return data

def save_data(data): #inserting data in json
    with open('patients.json',"w") as f:
        json.dump(data,f)


#to get all patients
@app.get('/view')
def view_all_data():
    data= load_data()

    return data
#using path paramtere now for specific patient

@app.get("/view/{patient_id}")
def view_one_patient(patient_id:str=Path(...,description="id of patient",example="101")):
    data=load_data()
    if(patient_id in data):
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient id not found")

#this was path parameter used to get data of a particular patient
#httpexception uses in fastapi to raise exception and status code properly
#path() is used to specify the path parameter clearly

#query paramter-is used to fetch data on filteration , (sorting basically)#they are optional
#it has query function to specify in more details
#400 status code = bad request


@app.get("/sort")
def view_filtered_data(
    sort_by: str = Query(
        description="Sort by age or weight",
        example="weight"
    ),
    order: str = Query("asc")
):

    valid_fields = ["age", "weight"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail="Can't sort with given parameter"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Sorry, can't sort in any other way"
        )

    data = load_data()

    sorted_records = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=(order == "desc")
    )

    return sorted_records


#using post method to receieve data -validate using pydantic model-if validated then insertion in json

#creation of a pydantic model
class Patient(BaseModel):
    id:Annotated[str,Field(...,description="it is to insert your patient i'd")]
    name:Annotated[str,Field(...,description="name of patient",example="abc..")]
    age:Annotated[int,Field(...,gt=0,lt=120)]
    weight:Annotated[float,Field(...,gt=0)]

    @computed_field
    @property
    def bmi(self)->float:
        return self.age+self.weight


#pydantic model-2 for data updation
class update_patient(BaseModel):
    name:Annotated[Optional[str],Field(description="name of patient",example="abc..",default=None   )]
    age:Annotated[Optional [int],Field(gt=0,lt=120,default=None)]
    weight:Annotated[Optional[float],Field(gt=0,default=None)]
    @computed_field
    @property
    def bmi(self)->float:
        if self.age is None or self.weight is None:
            return None
            return self.age + self.weight
  
@app.post("/create")
def create_patient(patient:Patient):
 
    #load existing data
    data=load_data()
    #check if patient already exist or not otheriwse add in database as new patient
    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient with i'd already exist")
    
    #now data is python dict and patient is a pydantic object
    #covert this pydantic obj. into a dict
    #add as new patient in data dict

    data[patient.id]=patient.model_dump(exclude=['id'])

    #saving finally this dict into json file

    save_data(data)
    return JSONResponse(status_code=201,content={"message":"your data is inserted successfully as a new patient"})

#update the patient
@app.put('/update/{patient_id}')
def patient_updated_info(patient_id:str,patient:update_patient):
    
    #data loading

    data=load_data()
    #if patient exits or not
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found!")
    
    existing_data = data[patient_id]
    #conversion of pydantic obj into a dictionary
    updated_data= patient.model_dump(exclude_unset=True)

    #updated values

    for key,value in updated_data.items():
        existing_data[key]=value

#now to update computed fields automatically as well
#exiting updated dict convert in pydantic
    existing_data['id']=patient_id
    obj1=Patient(**existing_data)
# object then again as dict then save data
    existing_data= obj1.model_dump(exclude={'id'})

    #add this dict to data now
    data[patient_id]=existing_data
#save the data
    save_data(data)
    return JSONResponse(status_code=200,content="updated successfully")



#delete the patient
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    #load data
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found!")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content="patient deleted successfully")


    











        


     
    
    






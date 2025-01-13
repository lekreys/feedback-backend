from fastapi import FastAPI , Depends, status , HTTPException , UploadFile , File , Form
from schemas import FeatureRequest , Bugs , Automations , Integrations , Languages , PublicAPI
import models
from database import Base , declarative_base , Sensionalocal, Engine , Client
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from typing import List



app = FastAPI()


# biar bisa buka dari localhost lain
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
    "http://localhost",  # Untuk localhost juga dapat diizinkan
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


Base.metadata.create_all(Engine)






def get_db():

    db= Sensionalocal() 

    try :
        yield db
    finally : 
        db.close()





################################ FEATURE REQUEST ##########################################
@app.get("/feature_request")
def get_feature_request(db : Session = Depends(get_db)):
    all_feedback = db.query(models.FeatureRequest).all()
    return all_feedback

@app.get("/feature_request/{id}")
def feature_request_by_id(id : int , db : Session = Depends(get_db)):
    feedback = db.query(models.FeatureRequest).where(models.FeatureRequest.id == id).first()
    if not feedback :
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Feature Request with the id {id} is not available")
    return feedback


@app.post("/feature_request/upload-file")
async def create_feature_request_upload_file(
    Title: str = Form(...),
    Description: str = Form(...),
    Category: str = Form(...),
    Vote: int = Form(...),
    images: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        for image in images:
            file_contents = await image.read()
            random_filename = f"{uuid4()}_{image.filename.replace(' ', '_')}"
            file_name = f"feature_request/{random_filename}"

            response = Client.storage.from_("feedback").upload(file_name, file_contents)

            public_url = Client.storage.from_("feedback").get_public_url(file_name)
            image_urls.append(public_url)

        new_feature =models.FeatureRequest(
            Title=Title,
            Description=Description,
            Category=Category,
            Vote=Vote,
            time_stamp=datetime.now(),
            image_url=image_urls  
        )

        db.add(new_feature)
        db.commit()
        db.refresh(new_feature)

        return new_feature

    except Exception as e:
        return {"error": f"Failed to upload images: {str(e)}"}



@app.post("/feature_request")
def post_feature_request(request : FeatureRequest , db : Session = Depends(get_db)) : 
    FeatureRequest = models.FeatureRequest(Title = request.Title , Description= request.Description , Category = request.Category , time_stamp=datetime.now() , Vote=request.Vote)
    db.add(FeatureRequest)
    db.commit()
    db.refresh(FeatureRequest)
    return FeatureRequest


@app.put("/feature_request/{id}")
def update_feature_request(id: int, request: FeatureRequest, db: Session = Depends(get_db)):

    FeatureRequest = db.query(models.FeatureRequest).filter(models.FeatureRequest.id == id).first()

    if FeatureRequest is None:
        raise HTTPException(status_code=404, detail="FeatureRequest not found")
    
    FeatureRequest.Title = request.Title
    FeatureRequest.Description = request.Description
    FeatureRequest.Category = request.Category
    FeatureRequest.Vote = request.Vote

    
    db.commit()
    db.refresh(FeatureRequest)  
    
    return {"message": f"Success Update data with id {id}", "data": FeatureRequest}







################################ BUGSSSSSSSSSSSSSS ####################################

@app.get("/bugs")
def get_bugs(db : Session = Depends(get_db)):
    all_bugs = db.query(models.Bugs).all()
    return all_bugs


@app.post("/bugs")
def post_bugs(request : Bugs , db : Session = Depends(get_db)) : 
    new_bug = models.Bugs(Title = request.Title , Description= request.Description , Category = request.Category , time_stamp=datetime.now() , Vote=0)
    db.add(new_bug)
    db.commit()
    db.refresh(new_bug)
    return new_bug



@app.post("/bugs/upload-file")
async def create_bugs_upload_file(
    Title: str = Form(...),
    Description: str = Form(...),
    Category: str = Form(...),
    Vote: int = Form(...),
    images: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        for image in images:
            file_contents = await image.read()
            random_filename = f"{uuid4()}_{image.filename.replace(' ', '_')}"
            file_name = f"bugs/{random_filename}"

            response = Client.storage.from_("feedback").upload(file_name, file_contents)

            public_url = Client.storage.from_("feedback").get_public_url(file_name)
            image_urls.append(public_url)

        # Simpan data ke database
        new_feature =models.Bugs(
            Title=Title,
            Description=Description,
            Category=Category,
            Vote=Vote,
            time_stamp=datetime.now(),
            image_url=image_urls  
        )

        db.add(new_feature)
        db.commit()
        db.refresh(new_feature)

        return new_feature

    except Exception as e:
        return {"error": f"Failed to upload images: {str(e)}"}



@app.get("/bugs/{id}")
def bugs_by_id(id : int , db : Session = Depends(get_db)):
    bugs = db.query(models.Bugs).where(models.Bugs.id == id).first()
    if not bugs :
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Feature Request with the id {id} is not available")
    return bugs



@app.put("/bugs/{id}")
def update_bugs(id: int, request: Bugs, db: Session = Depends(get_db)):
    bugs = db.query(models.Bugs).filter(models.Bugs.id == id).first()

    if bugs is None:
        raise HTTPException(status_code=404, detail="bugs not found")
    
    bugs.Title = request.Title
    bugs.Description = request.Description
    bugs.Category = request.Category
    bugs.Vote = request.Vote
    
    db.commit()
    db.refresh(bugs)  
    
    return {"message": f"Success Update data with id {id}", "data": bugs}


################################ Automations ####################################



@app.get("/automations")
def get_automations(db : Session = Depends(get_db)):
    all_automations = db.query(models.Automations).all()
    return all_automations


@app.post("/automations")
def post_automations(request : Automations , db : Session = Depends(get_db)) : 
    new_automations = models.Automations(Title = request.Title , Description= request.Description ,  time_stamp=datetime.now(), Vote=request.Vote)
    db.add(new_automations)
    db.commit()
    db.refresh(new_automations)
    return new_automations


@app.post("/automations/upload-file")
async def create_automations_upload_file(
    Title: str = Form(...),
    Description: str = Form(...),
    Vote: int = Form(...),
    images: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        for image in images:
            file_contents = await image.read()
            random_filename = f"{uuid4()}_{image.filename.replace(' ', '_')}"
            file_name = f"automations/{random_filename}"

            response = Client.storage.from_("feedback").upload(file_name, file_contents)

            public_url = Client.storage.from_("feedback").get_public_url(file_name)
            image_urls.append(public_url)

        new_feature =models.Automations(
            Title=Title,
            Description=Description,
            Vote=Vote,
            time_stamp=datetime.now(),
            image_url=image_urls  
        )

        db.add(new_feature)
        db.commit()
        db.refresh(new_feature)

        return new_feature

    except Exception as e:
        return {"error": f"Failed to upload images: {str(e)}"}





@app.get("/automations/{id}")
def automations_by_id(id : int , db : Session = Depends(get_db)):
    Automations = db.query(models.Automations).where(models.Automations.id == id).first()
    if not Automations :
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Automations with the id {id} is not available")
    return Automations



@app.put("/automations/{id}")
def update_automations(id: int, request: Automations, db: Session = Depends(get_db)):
    automations = db.query(models.Automations).filter(models.Automations.id == id).first()

    if automations is None:
        raise HTTPException(status_code=404, detail="Automations not found")
    
    automations.Title = request.Title
    automations.Description = request.Description
    automations.Vote = request.Vote
   
    
    db.commit()
    db.refresh(automations)  
    
    return {"message": f"Success Update data with id {id}", "data": automations}







################################ Integrations ####################################



@app.get("/integrations")
def get_integrations(db : Session = Depends(get_db)):
    Integrations = db.query(models.Integrations).all()
    return Integrations


@app.post("/integrations")
def post_integrations(request : Integrations , db : Session = Depends(get_db)) : 
    Integrations = models.Integrations(Title = request.Title , Description= request.Description , time_stamp=datetime.now() , Vote=0)
    db.add(Integrations)
    db.commit()
    db.refresh(Integrations)
    return Integrations



@app.post("/integrations/upload-file")
async def create_integrations_upload_file(
    Title: str = Form(...),
    Description: str = Form(...),
    Vote: int = Form(...),
    images: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        for image in images:
            file_contents = await image.read()
            random_filename = f"{uuid4()}_{image.filename.replace(' ', '_')}"
            file_name = f"integrations/{random_filename}"

            response = Client.storage.from_("feedback").upload(file_name, file_contents)

            public_url = Client.storage.from_("feedback").get_public_url(file_name)
            image_urls.append(public_url)

        new_feature =models.Integrations(
            Title=Title,
            Description=Description,
            Vote=Vote,
            time_stamp=datetime.now(),
            image_url=image_urls  
        )

        db.add(new_feature)
        db.commit()
        db.refresh(new_feature)

        return new_feature

    except Exception as e:
        return {"error": f"Failed to upload images: {str(e)}"}



@app.get("/integrations/{id}")
def integrations_by_id(id : int , db : Session = Depends(get_db)):
    Integrations = db.query(models.Integrations).where(models.Integrations.id == id).first()
    if not Integrations :
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Integrations with the id {id} is not available")
    return Integrations



@app.put("/integrations/{id}")
def update_integrations(id: int, request: Integrations, db: Session = Depends(get_db)):
    Integrations = db.query(models.Integrations).filter(models.Integrations.id == id).first()

    if Integrations is None:
        raise HTTPException(status_code=404, detail="Integrations not found")
    
    Integrations.Title = request.Title
    Integrations.Description = request.Description
    Integrations.Vote = request.Vote
   
    db.commit()
    db.refresh(Integrations)  
    
    return {"message": f"Success Update data with id {id}", "data": Integrations}





################################ Languages ####################################



@app.get("/languages")
def get_languages(db : Session = Depends(get_db)):
    Languages = db.query(models.Languages).all()
    return Languages


@app.post("/languages")
def post_languages(request : Languages , db : Session = Depends(get_db)) : 
    Languages = models.Languages(Title = request.Title , Description= request.Description , time_stamp=datetime.now() , Vote=0)
    db.add(Languages)
    db.commit()
    db.refresh(Languages)
    return Languages



@app.post("/languages/upload-file")
async def create_languages_upload_file(
    Title: str = Form(...),
    Description: str = Form(...),
    Vote: int = Form(...),
    images: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        for image in images:
            file_contents = await image.read()
            random_filename = f"{uuid4()}_{image.filename.replace(' ', '_')}"
            file_name = f"languages/{random_filename}"

            response = Client.storage.from_("feedback").upload(file_name, file_contents)

            public_url = Client.storage.from_("feedback").get_public_url(file_name)
            image_urls.append(public_url)

        new_feature =models.Languages(
            Title=Title,
            Description=Description,
            Vote=Vote,
            time_stamp=datetime.now(),
            image_url=image_urls  
        )

        db.add(new_feature)
        db.commit()
        db.refresh(new_feature)

        return new_feature

    except Exception as e:
        return {"error": f"Failed to upload images: {str(e)}"}



@app.get("/languages/{id}")
def languages_by_id(id : int , db : Session = Depends(get_db)):
    Languages = db.query(models.Languages).where(models.Languages.id == id).first()
    if not Languages :
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Languages with the id {id} is not available")
    return Languages



@app.put("/languages/{id}")
def update_languages(id: int, request: Languages, db: Session = Depends(get_db)):
    Languages = db.query(models.Languages).filter(models.Languages.id == id).first()

    if Languages is None:
        raise HTTPException(status_code=404, detail="Languages not found")
    
    Languages.Title = request.Title
    Languages.Description = request.Description
    Languages.Vote = request.Vote
   
    db.commit()
    db.refresh(Languages)  
    
    return {"message": f"Success Update data with id {id}", "data": Languages}





################################ Public API ####################################



@app.get("/public_api")
def get_public_api(db : Session = Depends(get_db)):
    PublicAPI = db.query(models.PublicAPI).all()
    return PublicAPI


@app.post("/public_api")
def post_public_api(request : PublicAPI , db : Session = Depends(get_db)) : 
    PublicAPI = models.PublicAPI(Title = request.Title , Description= request.Description , Category=request.Category , time_stamp=datetime.now() , Vote=0)
    db.add(PublicAPI)
    db.commit()
    db.refresh(PublicAPI)
    return PublicAPI



@app.post("/public_api/upload-file")
async def create_public_api_upload_file(
    Title: str = Form(...),
    Description: str = Form(...),
    Category: str = Form(...),
    Vote: int = Form(...),
    images: List[UploadFile] = File(...),  
    db: Session = Depends(get_db)
):
    try:
        image_urls = []

        for image in images:
            file_contents = await image.read()
            random_filename = f"{uuid4()}_{image.filename.replace(' ', '_')}"
            file_name = f"public_api/{random_filename}"

            response = Client.storage.from_("feedback").upload(file_name, file_contents)

            public_url = Client.storage.from_("feedback").get_public_url(file_name)
            image_urls.append(public_url)

        new_feature =models.PublicAPI(
            Title=Title,
            Description=Description,
            Category=Category,
            Vote=Vote,
            time_stamp=datetime.now(),
            image_url=image_urls 
        )

        db.add(new_feature)
        db.commit()
        db.refresh(new_feature)

        return new_feature

    except Exception as e:
        return {"error": f"Failed to upload images: {str(e)}"}


@app.get("/public_api/{id}")
def feature_request_by_id(id : int , db : Session = Depends(get_db)):
    PublicAPI = db.query(models.PublicAPI).where(models.PublicAPI.id == id).first()
    if not PublicAPI :
       
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"PublicAPI with the id {id} is not available")
    return PublicAPI



@app.put("/public_api/{id}")
def update_feature_request(id: int, request: PublicAPI, db: Session = Depends(get_db)):
    PublicAPI = db.query(models.PublicAPI).filter(models.PublicAPI.id == id).first()

    if PublicAPI is None:
        raise HTTPException(status_code=404, detail="Languages not found")
    
    PublicAPI.Title = request.Title
    PublicAPI.Description = request.Description
    PublicAPI.Category = request.Category
    PublicAPI.Vote = request.Vote
   
    db.commit()
    db.refresh(PublicAPI)  
    
    return {"message": f"Success Update data with id {id}", "data": PublicAPI}

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

from sqlalchemy.future import select

app = FastAPI()


DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    field_data = Column(String, index=True)


engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/api/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/submit/")
# async def submit_data(field_data: str = Form(...)):
#     async with database.transaction():
#         # Insert new data
#         query = Data.__table__.insert().values(field_data=field_data)
#         last_record_id = await database.execute(query)
        
#         # Retrieve the last inserted data using the returned primary key
#         query = select(Data).where(Data.id == last_record_id)
#         last_record = await database.fetch_one(query)
        
#         # Check if data is correctly saved
#         if last_record and last_record.field_data == field_data:
#             return {"success": "Data saved successfully", "data": last_record.field_data}
#         else:
#             return {"error": "Data was not saved correctly"}

@app.get("/api/form/")
async def form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/api/submit/")
async def submit_data(field_data: str = Form(...)):
    async with database.transaction():
        query = Data.__table__.insert().values(field_data=field_data)
        await database.execute(query)
    return {"success": "Data saved successfully"}



@app.post("/api/async-submit/")
async def async_submit_data(field_data: str = Form(...)):
    async with database.transaction():

        query = Data.__table__.insert().values(field_data=field_data)
        await database.execute(query)
    
    return {"success": "Data saved successfully"}


@app.get("/api/async-form/")
async def async_form(request: Request):
    return templates.TemplateResponse("async_form.html", {"request": request})


#below verification if data added to db

# @app.post("/async-submit/")
# async def async_submit_data(field_data: str = Form(...)):
#     async with database.transaction():

#         query = Data.__table__.insert().values(field_data=field_data)
#         last_record_id = await database.execute(query)
        

#         query = select(Data).where(Data.id == last_record_id)
#         last_record = await database.fetch_one(query)


#         if last_record:
#             return {"success": "Data saved successfully", "data": last_record.field_data}
#         else:
#             return {"error": "Data was not saved correctly"}




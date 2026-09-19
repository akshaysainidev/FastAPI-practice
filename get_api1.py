from fastapi import FastAPI, File, Form, UploadFile, Header,Cookie,Response
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI() # create app instance of fastapi

class Books(BaseModel):
    id: int
    b_name: str
    auther_name: str
    pg_count: int

bookList: List[Books]=[]

@app.get("/")
def book_health_check():
    return {"msg":"Health check complete , Books API is working"}

@app.get("/get_book_list")
def get_book_list():
    return {"details":bookList}

@app.post("/post_book")
def insert_Book(book_obj:Books):
    bookList.append(book_obj)
    return bookList

@app.put("/update_book")
def update_book_list(book_id:int,new_book_obj:Books):
    for idx,book in enumerate(bookList):
        if book.id == book_id:
            bookList[idx] = new_book_obj
            return bookList[idx]
    return {"Error": "Book not found"}
        
@app.delete("/delete_book")
def delete_Book(book_id:int):
    for idx,book in enumerate(bookList):
        if book.id == book_id:
            deleted_book = bookList.pop(idx)
            return {"msg":f"${deleted_book} is deleted"}
    return {"Error":"Unable to delete book"}

#response model (for structuring api response)
class BookResponse(BaseModel):
    id: int
    b_name: str

@app.post("/create_book_by_response_model2",response_model=BookResponse) #this will allow the api to return an book_obj with only 2 details
def create_book_2(book_obj:Books):
    bookList.append(book_obj)
    return book_obj # we need to return book_obj as response model needs an object

@app.post("/create_book_by_response_model3",response_model=list[BookResponse]) # only allow list of obj with 2 details only
def create_book3(book_obj:Books):
    bookList.append(book_obj)
    return bookList # now we can return the booklist as the response model takes list of book objects 

#form data and file upload (to deal with HTML forms)
@app.post("/submit_form")
async def purchase_book(
        title:str=Form(...), # The ... means the client must send title (required)
        #but removing ... doesn't make title to be non default (optional) bcz str means the value cannot be None, and Form() doesn't provide a default value. so to actually make it optional we need to use like     
        #title: Optional[str] = Form(None), or  #title: str = Form(None), 
        file:UploadFile = File(None) # here if we remove None then giving a file is mendatory
    ):   
        result = {"title":title,"filename":file.filename if file else "None"}
        return result

# headers and cookies


def main():
    print("Starting the server")
    uvicorn.run(app,host="127.0.0.1",port=8000) #we can also run server like this 
    # but we follow this uvicorn main:app --reload to automaically reload the server if any changes 


if __name__ == "__main__":
    main()


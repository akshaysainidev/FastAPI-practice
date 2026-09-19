from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
app=FastAPI()

class Books(BaseModel):
    id: int
    name: str
    author: str

bookList:List[Books]=[]


@app.get('/')
async def read_root():
    return {"msg":"Welcome to the book store"}

@app.get('/books')
def read_books():
    return bookList

@app.post('/books')
def add_book(book_name:Books):
    bookList.append(book_name)
    return bookList

@app.put('/books/{book_id}')
def edit_book(book_id: int, new_book_name: Books):
    for idx, book in enumerate(bookList):
        if book.id == book_id:
            bookList[idx]=new_book_name
            # bookList[idx].id=new_book_name.id
            # bookList[idx].name = new_book_name.name
            # bookList[idx].author=new_book_name.author
            return bookList[idx]
    return {"Error": "Book not found"}


@app.delete('/books/{book_id}')
def delete_book(book_id:int):
    for idx,book in enumerate(bookList):
        if(book.id==book_id):
            deleted_book=bookList.pop(idx)
            return {"msg":f"${deleted_book} is deleted"}
    return {"Error":"No book found"}



def main():
    print("Hello from fast-api!")

if __name__ == "__main__":
    main()

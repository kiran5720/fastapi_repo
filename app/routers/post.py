
from .. import models,schemas,utils,oauth2
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from typing import Union,Optional,List
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine,get_db


router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

#response_model=List[schemas.Post]
@router.get("/",response_model=List[schemas.PostOut])
def read_root(db:Session = Depends(get_db),
              curr_user: int = Depends(oauth2.get_current_user),limit : int = 10,
              skip:int = 0,search:Optional[str] = ""):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter =True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # formatted_results = [
    #     schemas.PostOut(Postt=result[0], votes=result[1])  # result[0] is Post, result[1] is votes
    #     for result in results
    # ]

    return posts

@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def post_item(post: schemas.PostBase,db:Session=Depends(get_db),
              curr_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(curr_user.id)
    post.dict()
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(owner_id = curr_user.id, **post.dict())  # (the ** post.dict will do the above thing in easier way)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db),
             curr_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter =True).group_by(models.Post.id).filter(models.Post.id==id).first()
    
    print(posts)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'id not found{id}')
    return posts

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),
                curr_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id:{id} doesnt exist")
    
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform requested auction")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostUpdate,db:Session = Depends(get_db),
                curr_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s 
    #                RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id:{id} doesnt exist")
    
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorised to perform requested auction")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()

    return post_query.first()


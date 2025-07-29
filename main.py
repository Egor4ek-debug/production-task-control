from fastapi import FastAPI


from api import batches
from api import products
from api import work_center
app = FastAPI()


app.include_router(batches.router)
app.include_router(products.router)
app.include_router(work_center.router)

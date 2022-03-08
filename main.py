from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'Data': {'Name': 'Yolo'}}


@app.get('/about')
def about():
    return {'Data': {'About Page'}}

from fastapi import FastAPI

app = FastAPI(
    title='Trading App'
)


@app.get('/')
async def index():
    return {'text': 'Hello, World!'}
from fastapi import FastAPI
import httpx

app = FastAPI()

JOKE_API_URL = 'https://official-joke-api.appspot.com/random_joke'

@app.get('/joke')
async def get_joke():
    async with httpx.AsyncClient() as client:
        response = await client.get(JOKE_API_URL)
        joke = response.json()
        return {'setup': joke['setup'], 'punchline': joke['punchline']}

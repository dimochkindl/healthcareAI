import os
from core.http import create_response
from datetime import datetime
from fastapi import APIRouter
from models.business_data import Content
from repository.tools import bordering_text
from repository.assistant import GigaChatAPI
from repository.database.business_data import BusinessDataRepository


router = APIRouter()


@router.post("/")
async def save_content_embedding(data: Content):
    giga = GigaChatAPI()
    text = data.text
    bordered = bordering_text(text=text)
    embeds = []

    for each_text in bordered:
        embed = await giga.create_embeddings(text=each_text)
        print(embed["data"][0]["embedding"])
        await BusinessDataRepository.create({"embedding": embed["data"][0]["embedding"], "text": each_text})
        embeds.append(embed)

    return embeds

@router.post("/search")
async def search_content(data: Content):
    giga = GigaChatAPI()
    embed = await giga.create_embeddings(text=data.text)
    results = await BusinessDataRepository.get_by_closest_l2_distance(embed["data"][0]["embedding"])

    return results

@router.get("/save_food_embeddings")
async def save_food_embeddings():
    giga = GigaChatAPI()
    for dirpath, directory_names, files_names in os.walk("docs"):
        for filename in files_names:
            print(filename)
            with open(os.path.join(dirpath, filename), 'r') as f:
                text = f.readlines()
                bordered = bordering_text(text=str(text))

                embeds = []
                for each_text in bordered:
                    embed = await giga.create_embeddings(text=each_text)
                    await BusinessDataRepository.create({"embedding": embed["data"][0]["embedding"], "text": each_text})
                    embeds.append(embed)


    return await create_response(code=200, data=f'Embeddings saved {datetime.now()}')

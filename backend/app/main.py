import asyncio
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routers.flipkart_scraper import FlipkartScrapper

class RequestSchema(BaseModel):
    url: str
    pageNumber: int

app = FastAPI(title="Extract reviews from e-commerse website")

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health-check")
async def health_check():
    return {"message": "Hello, Welcome to web scrapping portal!"}


@app.post("/api/extract-reviews")
async def extract_reviews(details: RequestSchema):
    url = details.url
    loop = asyncio.get_event_loop()
    if "flipkart.com" in url:
        reviews = await loop.run_in_executor(None, FlipkartScrapper(url).extract_reviews, details.pageNumber)
    elif "amazon.com" or "amazon.in" in url:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"success": False, "message": "Enter flipkart URL only. To get review for amazon run manual scripts."}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"success": False, "message": "Invalid product URL"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"success": True, "content": jsonable_encoder(reviews)}
    )
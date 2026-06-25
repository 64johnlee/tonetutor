from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from seo_pages import PAGES as SEO_PAGES
from api.chat import router as chat_router
from api.copilot import router as copilot_router
from api.session import router as session_router
from api.transcribe import router as transcribe_router
from api.tts import router as tts_router
from api.billing import router as billing_router
from api.events import router as events_router

app = FastAPI(title="ToneTutor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(copilot_router)
app.include_router(session_router)
app.include_router(transcribe_router)
app.include_router(tts_router)
app.include_router(billing_router)
app.include_router(events_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html", headers={"Cache-Control": "no-store"})


@app.get("/hsk-speaking-test")
async def hsk_speaking_test():
    # SEO landing page (cacheable, unlike the no-store SPA) targeting "HSK speaking test" search intent
    return FileResponse("static/hsk-speaking-test.html")


@app.get("/robots.txt")
async def robots():
    return Response(
        "User-agent: *\nAllow: /\nSitemap: https://tonetutor.tefusiang.com/sitemap.xml\n",
        media_type="text/plain",
    )


@app.get("/sitemap.xml")
async def sitemap():
    base = "https://tonetutor.tefusiang.com"
    locs = [(f"{base}/", "weekly", "1.0"),
            (f"{base}/hsk-speaking-test", "monthly", "0.9")]
    locs += [(f"{base}/{slug}", "monthly", "0.8") for slug in SEO_PAGES]
    rows = "".join(
        f'  <url><loc>{loc}</loc><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n'
        for loc, cf, pr in locs
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           f'{rows}</urlset>\n')
    return Response(xml, media_type="application/xml")


@app.get("/health")
async def health():
    return {"status": "ok"}


# Keep this LAST: single-segment SEO landing pages (specific routes above win first).
@app.get("/{slug}")
async def seo_landing(slug: str):
    html = SEO_PAGES.get(slug)
    if html is None:
        raise HTTPException(status_code=404)
    return Response(html, media_type="text/html")

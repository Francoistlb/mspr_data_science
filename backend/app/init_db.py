import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from backend.app.core.database import Base, engine
from backend.app.models import models 

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())

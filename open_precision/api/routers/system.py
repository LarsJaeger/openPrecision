from fastapi import APIRouter

system_router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[]
)

@system_router.get("/config")
def get_config():
    # TODO: Implement this
    return {"config": "config"}
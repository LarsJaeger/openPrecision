router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

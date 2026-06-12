from handlers.tasks import router as tasks_router
from handlers.ping import router as ping_router

routers = [tasks_router, ping_router]
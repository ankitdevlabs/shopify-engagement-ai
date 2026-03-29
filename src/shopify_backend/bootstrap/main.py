from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from shopify_backend.configs.settings import get_application_settings
from shopify_backend.configs.constants import API_PREFIX
from shopify_backend.routes import engagement


class ShopifyApplication:
    def __init__(self):
        """Initialize Main"""
        self.settings = get_application_settings()

    def initialize_app(self) -> FastAPI:
        """Initialize Fast Api APP"""
        app = FastAPI(debug=self.settings.debug)

        app.state.settings = self.settings
        self.load_middlewares(app)
        self.load_routes(app)

        return app

    def load_middlewares(self, app: FastAPI) -> None:

        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.cors_allow_origins,
            allow_methods=list(self.settings.cors_allow_methods),
            allow_headers=self.settings.cors_allow_headers,
            allow_credentials=self.settings.cors_allow_credentials,
            max_age=self.settings.cors_max_age,
        )

    def load_routes(self, app: FastAPI) -> None:
        app.include_router(engagement.router, prefix=f"{API_PREFIX}/engagement")

    def app_context(self):
        pass

    def init_database(self):
        pass


app = ShopifyApplication().initialize_app()

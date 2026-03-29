from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from shopify_backend.configs.settings import get_application_settings


class ShopifyApplication:
    def __init__(self):
        """Initialize Main"""
        self.settings = get_application_settings()

    def initialize_app(self) -> FastAPI:
        """Initialize Fast Api APP"""
        app = FastAPI(
            debug=True,
            middleware=self.load_default_middlewares(),
            on_startup=[],
            on_shutdown=[],
        )

        self.load_routes(app)

        return app

    def load_routes(self, app: FastAPI) -> None:
        return []

    def app_context(self):
        pass

    def load_default_middlewares(self) -> list[Middleware]:
        middleware: list[Middleware] = []

        middleware.append(
            Middleware(
                CORSMiddleware,
                allow_origins=self.settings.cors_allow_origins,
                allow_methods=list(self.settings.cors_allow_methods),
                allow_headers=self.settings.cors_allow_headers,
                allow_credentials=self.settings.cors_allow_credentials,
                max_age=self.settings.cors_max_age,
            )
        )
        return middleware
    
    def init_database(self):
        pass


app = ShopifyApplication().initialize_app()
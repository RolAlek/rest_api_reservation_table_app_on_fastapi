from aioinject import Scoped

from application.core.infrastructure.di._types import Providers
from repositories.modules.table.table import _TableRepository

PROVIDERS: Providers = [Scoped(_TableRepository)]

import coreapi

from .company import schema as company_schema

documentation = coreapi.Document(
    title='Interview360 API',
    url='/api/v1/',
    content={
        'Companies': company_schema
    }
)

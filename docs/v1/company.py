import coreapi
import coreschema

list_link = coreapi.Link(
    url='/companies',
    action='get',
    description='Return list of companies for current user'
)
create_link = coreapi.Link(
    url='/companies',
    action='post',
    description='Create new company',
    fields=[
        coreapi.Field(
            'Authorization',
            required=True,
            location="header",
            description='Authorization header',
            schema=coreschema.String()
        ),
        coreapi.Field(
            'name',
            required=True,
            location="form",
            description='Company\'s name',
            schema=coreschema.String()
        ),
        coreapi.Field(
            'description',
            required=True,
            location="form",
            description='Company\'s description',
            schema=coreschema.String()
        ),
        coreapi.Field(
            'start_date',
            required=True,
            location="form",
            description='Company\'s start_date',
            schema=coreschema.String()
        ),
    ]
)
list_response = {
    '200': {
        'description': 'Success response',
        'schema': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {
                        'type': 'integer'
                    }
                }
            }
        }
    }
}

create_response = {
    '200': {
        'description': 'Success response',
        'schema': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'integer'
                }
            }
        }
    },
    '400': {
        'description': 'Failed response'
    }
}

list_link._responses_docs = list_response
create_link._responses_docs = create_response

schema = {
    'list': list_link,
    'create': create_link
}

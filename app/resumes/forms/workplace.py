from . import  BaseForm, cerberus, Resume, Workplace, Company, transaction

def resume_exist(field, value, error):
    """ Check wheter or not resume exist """

    try:
        resume = Resume.objects.get(id=value)
    except Resume.DoesNotExist:
        error(field, 'Does not exist')

class WorkplaceForm(BaseForm):
    """ Workplace form class """

    schema = {
        'workplaces': {
            'required': True,
            'empty': False,
            'type': 'list',
            'schema': {
                'required': True,
                'empty': False,
                'type': 'dict',
                'schema': {
                    'id': {
                        'type': 'integer',
                        'required': False
                    },
                    'position': {
                        'type': 'string',
                        'empty': False,
                        'required': True
                    },
                    'resume_id': {
                        'type': 'integer',
                        'empty': False,
                        'required': True,
                        'validator': resume_exist
                    },
                    'company': {
                        'type': 'string',
                        'empty': False,
                        'required': True
                    },
                    'description': {
                        'type': 'string',
                        'empty': False,
                        'required': True
                    },
                    'start_date': {
                        'type': 'string',
                        'regex': '^\d{4}-\d{2}-\d{2}$',
                        'empty': False,
                        'required': True
                    },
                    'end_date': {
                        'type': 'string',
                        'regex': '^\d{4}-\d{2}-\d{2}$',
                        'required': True
                    }
                }
            }
        }
    }

    def submit(self):
        """ Check the from validation and create workplaces """

        if not self.is_valid(): return False

        with transaction.atomic():
            response_list = []
            workplaces = self.params.get('workplaces')

            for wp in workplaces:
                company_name = wp.pop('company')
                company, created = Company.objects.get_or_create(name=company_name)
                if wp.get('id'):
                    workplace = Workplace.objects.get(id=wp.get('id'))
                    for key, value in wp.items():
                        setattr(workplace, key, value)
                else:
                    workplace = Workplace.objects.create(**wp, company=company)
                response_list.append(workplace)
            self.objects = response_list
            return True

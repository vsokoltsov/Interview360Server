from . import  (
    BaseForm, FormException, cerberus, Resume, Workplace, Company,
    transaction, WorkplaceForm
)
import ipdb

class ResumeForm(BaseForm):
    """
    Resume form object.
    :param title: Resume title
    :param description: Resume description
    :param skills: List of skills for resume
    :param salary: Salary value for resume
    :param user_id: Id of the user, to whom this resume belongs to
    :return True/False whether form was submitted
    """

    schema = {
        'id': {
            'type': 'integer',
            'required': False
        },
        'title': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'description': {
            'type': 'string',
            'empty': False,
            'required': True
        },
        'skills': {
            'type': 'list',
            'schema': {
                'type': 'integer'
            }
        },
        'salary': {
            'type': 'float',
            'required': True
        },
        'user_id': {
            'type': 'integer',
            'required': True
        },
        'workplaces': {
            'type': 'list',
            'required': True,
            'empty': False
        }
    }

    def submit(self):
        """
        Create or update resume;
        Set skills to resume object;
        Set workplaces to resume object;
        """

        if not self.is_valid():
            return False

        try:
            with transaction.atomic():
                workplaces = self.params.pop('workplaces', [])
                skills = self.params.pop('skills', [])
                self._set_attributes()
                self.obj.skills.set(skills)
                workplace_form = WorkplaceForm(params={ 'workplaces': workplaces })
                if not workplace_form.submit():
                    raise FormException(
                        field='workplaces', errors=workplace_form.errors
                    )
                return True
        except FormException as e:
            self.errors = {
                **self.errors,
                **e.errors
            }
            return False


    def _set_attributes(self):
        for field, value in self.params.items():
            setattr(self.obj, field, value)
        self.obj.save()

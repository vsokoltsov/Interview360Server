from .models import Resume

def resume_exist(field, value, error):
    """ Check wheter or not resume exist """

    try:
        resume = Resume.objects.get(id=value)
    except Resume.DoesNotExist:
        error(field, 'Does not exist')

from companies.models import Company


def company_exist(field, value, error):
    """Check whether or not company exist."""

    try:
        return Company.objects.get(id=value)
    except Company.DoesNotExist:
        error(field, 'Does not exist')

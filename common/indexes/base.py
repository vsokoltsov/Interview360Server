from companies.index import CompanyIndex
from resumes.index import ResumesIndex
from skills.index import SkillIndex
from profiles.index import UserIndex
from vacancies.index import VacancyIndex
from specialties.index import SpecialtyIndex

def init_indexes():
    """ Init  existing indexes """

    for item in [
        CompanyIndex, ResumesIndex, SkillIndex, UserIndex, VacancyIndex,
        SpecialtyIndex
        ]:
        try:
            item.init()
        except:
            pass

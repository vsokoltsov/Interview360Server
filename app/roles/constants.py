COMPANY_OWNER = 1
HR = 2
CANDIDATE = 3
EMPLOYEE = 4

ROLE_IDENTIFIERS = {
    "{}".format(COMPANY_OWNER): 'CompanyOwner',
    "{}".format(HR): 'Hr',
    "{}".format(CANDIDATE): 'Candidate',
    "{}".format(EMPLOYEE): 'Employee'
}
RECEIVE_COMPANY = 'receive_company'
UPDATE_COMPANY = 'update_company'
DELETE_COMPANY = 'delete_company'

ADD_EMPLOYEE_TO_COMPANY = 'add_employee_to_company'
RECEIVE_EMPLOYEES = 'receive_employees'
DELETE_EMPLOYEES = 'delete_employee'

RECEIVE_VACANCY = 'receive_vacancy'
CREATE_VACANCY = 'create_vacancy'
UPDATE_VACANCY = 'update_vacancy'
DELETE_VACANCY = 'delete_vacancy'

RECEIVE_INTERVIEW = 'receive_interview'
CREATE_INTERVIEW = 'create_interview'
UPDATE_INTERVIEW = 'update_interview'
DELETE_INTERVIEW = 'delete_interview'
PARTICIPATE_INTERVIEW = 'participate_interview'
ADD_EMPLOYEE_TO_INTERVIEW = 'add_employee_to_interview'

CREATE_FEEDBACK = 'create_feedback'
UPDATE_FEEDBACK = 'update_feedback'
DELETE_FEEDBACK = 'delete_feedback'

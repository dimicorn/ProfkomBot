import gspread
import constants as const

# Column numbers starts with 1. Column A <=> 1'st column
EMAIL_COLUMN = 1

# Column with 1 and 0. 1 means IN_PROFKOM, 0 means OUT_PROFKOM
IN_PROFKOM_STATUS_COLUMN = 13

def find_user_in_profkom_list(email):
    sa = gspread.service_account(filename=const.files["profkomlist_config"])
    sh = sa.open("Список членов Профсоюза МФТИ")
    wks = sh.worksheet("Итог")
    all_emails = wks.col_values(EMAIL_COLUMN)
    for i in range(len(all_emails)):
        if all_emails[i] == email:
            if wks.cell(i+1, IN_PROFKOM_STATUS_COLUMN).value == '1':
                return True
    return False

COMPANY_NAME_COLUMN = 1
COMPANY_DISCR_COLUMN = 2
COMPANY_TUTORIAL_COLUMN = 3
COMPANY_ENDDATE_COLUMN = 4

def load_bonuses():
    sa = gspread.service_account(filename=const.files["bonus_config"])
    sh = sa.open("Возможности Профкома")
    wks = sh.worksheet("Main")
    companies = wks.col_values(COMPANY_NAME_COLUMN)
    discrs    = wks.col_values(COMPANY_DISCR_COLUMN)
    tutorials = wks.col_values(COMPANY_TUTORIAL_COLUMN)
    enddates  = wks.col_values(COMPANY_ENDDATE_COLUMN)
    
    return [companies[1:], discrs[1:], tutorials[1:], enddates[1:]]



if __name__ == "__main__":
    print(load_bonuses())
    print("You're running the wrong file!")

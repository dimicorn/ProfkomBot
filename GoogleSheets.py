import gspread


def find_user(email):
    sa = gspread.service_account(filename="config2.json")
    sh = sa.open("Список членов Профсоюза МФТИ")
    wks = sh.worksheet("Итог")
    all_emails = wks.col_values(10)
    for i in range(len(all_emails)):
        if all_emails[i] == email:
            if wks.acell('D' + str(i+1)).value == '1':
                return True
    return False


if __name__ == "__main__":
    print("You're running the wrong file!")

import gspread


sa = gspread.service_account(filename="config2.json")
sh = sa.open("Список членов Профсоюза МФТИ")

# wks = sh.worksheet("Итог")


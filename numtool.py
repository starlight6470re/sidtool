import datetime
def calculate_date_from_num(num):
    unix_time_str = num[2:] #後ろ8桁を日付計算に利用
    unix_time = int(unix_time_str)*100
    date = datetime.datetime.fromtimestamp(unix_time)
    return date.year, date.month, date.day
while True:
    while True:
        try:
            num = str(input("10桁の数字を入力してください: "))
            tmp = int(num)
            break
        except ValueError:
            print("数値以外が入力されています。")
    if len(num)<10:
         print("10桁未満です。") 
    else:
         break
year, month, day = calculate_date_from_num(num)
print ("日付は"+str(year)+"/"+str(month)+"/"+str(day))
print ("または"+str(year)+"/"+str(month)+"/"+str(day+1))

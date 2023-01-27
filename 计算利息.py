from servers.consol import consol

rice = 10000

for index in range(365):
    lixi = rice * 0.001
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D1 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10

i = 0
while rice < 100:
    lixi = rice * 0.001
    rice += lixi
    i += 1

rice = 10000
for index in range(365 // 5):
    lixi = rice * 0.01
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D5 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 10):
    lixi = rice * 0.011
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D10 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 30):
    lixi = rice * 0.12
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D30 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 60):
    lixi = rice * 0.3
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D60 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 90):
    lixi = rice * 0.54
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D90 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 180):
    lixi = rice * 1.45
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D180 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 360):
    lixi = rice * 5.5
    rice += lixi

consol.suc('一年时间投资 10000U 的情况下, USDT D360 的盈利金额为：%f 复利的年化率：%f' %
           (rice - 10000, (rice / 10000) - 1))

vip_2 = 1000
vip_3 = 5000
vip_4 = 10000
vip_5 = 50000
vip_6 = 100000
vip_7 = 200000
vip_8 = 400000
vip_9 = 800000
vip_10 = 1600000

day = 0
water = 0
cat_price = 160
interest = 0.025

if cat_price == 10:
    interest = 0.025
elif cat_price == 40:
    interest = 0.0275
elif cat_price == 160:
    interest = 0.03
elif cat_price == 640:
    interest = 0.0325
else:
    interest = 0.035

while water < vip_2:
    day += 1
    water += cat_price + cat_price * interest
consol.suc('%d 块钱，刷到VIP2，需要：%d天' % (cat_price, day))

while water < vip_3:
    day += 1
    water += cat_price + cat_price * interest * 2
consol.suc('%d 块钱，刷到VIP3，需要：%d天' % (cat_price, day))

while water < vip_4:
    day += 1
    water += cat_price + cat_price * interest * 3
consol.suc('%d 块钱，刷到VIP4，需要：%d天' % (cat_price, day))

while water < vip_5:
    day += 1
    water += cat_price + cat_price * interest * 4
consol.suc('%d 块钱，刷到VIP5，需要：%d天' % (cat_price, day))

while water < vip_6:
    day += 1
    water += cat_price + cat_price * interest * 5
consol.suc('%d 块钱，刷到VIP6，需要：%d天' % (cat_price, day))

while water < vip_7:
    day += 1
    water += cat_price + cat_price * interest * 6
consol.suc('%d 块钱，刷到VIP7，需要：%d天' % (cat_price, day))

while water < vip_8:
    day += 1
    water += cat_price + cat_price * interest * 7
consol.suc('%d 块钱，刷到VIP8，需要：%d天' % (cat_price, day))

while water < vip_9:
    day += 1
    water += cat_price + cat_price * interest * 8
consol.suc('%d 块钱，刷到VIP9，需要：%d天' % (cat_price, day))

while water < vip_10:
    day += 1
    water += cat_price + cat_price * interest * 9
consol.suc('%d 块钱，刷到VIP10，需要：%d天' % (cat_price, day))

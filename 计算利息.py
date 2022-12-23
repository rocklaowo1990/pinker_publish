from servers.consol import consol

rice = 10000

for index in range(365):
    lixi = rice * 0.001
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D1 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10

i = 0
while rice < 100:
    lixi = rice * 0.001
    rice += lixi
    i += 1

print(i / 365, rice)

rice = 10000
for index in range(365 // 5):
    lixi = rice * 0.01
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D5 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 10):
    lixi = rice * 0.03
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D10 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 30):
    lixi = rice * 0.12
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D30 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 60):
    lixi = rice * 0.3
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D60 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 90):
    lixi = rice * 0.9
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D90 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 180):
    lixi = rice * 1.89
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D180 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

rice = 10000
for index in range(365 // 360):
    lixi = rice * 3.96
    rice += lixi

consol.success('一年时间投资 10000U 的情况下, USDT D360 的盈利金额为：%f 复利的年化率：%f' %
               (rice - 10000, (rice / 10000) - 1))

from curses.ascii import isblank
import random

ci: int = 0
prcie_all: int = 0

for i in range(0, 400):
    prcie_single = 0

    isBreak = True
    while isBreak:
        prcie_all += 20
        prcie_single += 20
        suss_random = random.randint(0, 9)
        if (suss_random == 1):
            ci += 1
            break
    print('第 %d 次成功用了 %d 个黑钻（尝试了 %d 次）' % (i, prcie_single, prcie_single / 20))

print('一共尝试了 %d 次，成功了 %d 次，单次消耗：%d 钻石' % (prcie_all / 20, ci, prcie_all / ci))

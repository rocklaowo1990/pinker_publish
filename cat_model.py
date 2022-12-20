#-----------------------------------------------------------------------------------
# 概率模型
# 1人1天最多可以收集10次，1个月收集300次，1万个人总共收集 300万次
# lenght: 收集的总次数
#-----------------------------------------------------------------------------------
import random

drop_length = 300

#-----------------------------------------------------------------------------------
# 装备模型：
# id                道具名称                掉落概率                说明
# 0                 逗猫器                  6%                     -10% 收集CD
# 1                 捕鼠玩具                3%                     -20% 收集CD
# 2                 钓鱼棒                  2%                     -30% 收集CD
# 3                 逗猫法杖                0.9%                   -50% 收集CD
# 4                 汤姆的神杖              0.1%                    -100% 收集CD
# 5                 合成加速卡              38%                     -5% 合成CD
# 6                 猫魂水晶                6%                     +10% 收集效果
# 7                 琥珀精华                3%                     +20% 收集效果
# 8                 魔法水晶                2%                     +30% 收集效果
# 9                 九尾猫之魂              0.9%                   +50% 收集效果
# 10                蓝魔之泪                0.1%                   +100% 收集效果
# 11                森林精华                38%                     +5% 合成概率
#-----------------------------------------------------------------------------------
props_data = [
    {
        'id': 0,
        'name': '逗猫棒',
        'info': '-10% 收集CD',
        'probability': 0.06,
    },
    {
        'id': 1,
        'name': '捕鼠玩具',
        'info': '-20% 收集CD',
        'probability': 0.03,
    },
    {
        'id': 2,
        'name': '钓鱼棒',
        'info': '-30% 收集CD',
        'probability': 0.02,
    },
    {
        'id': 3,
        'name': '逗猫法杖',
        'info': '-50% 收集CD',
        'probability': 0.009,
    },
    {
        'id': 4,
        'name': '汤姆的神杖',
        'info': '-100% 收集CD',
        'probability': 0.001,
    },
    {
        'id': 5,
        'name': '合成加速卡',
        'info': '-5% 合成CD',
        'probability': 0.38,
    },
    {
        'id': 6,
        'name': '猫魂水晶',
        'info': '+10% 收集效果',
        'probability': 0.06,
    },
    {
        'id': 7,
        'name': '琥珀精华',
        'info': '+20% 收集效果',
        'probability': 0.03,
    },
    {
        'id': 8,
        'name': '魔法水晶',
        'info': '+30% 收集效果',
        'probability': 0.02,
    },
    {
        'id': 9,
        'name': '九尾猫之魂',
        'info': '+50% 收集效果',
        'probability': 0.009,
    },
    {
        'id': 10,
        'name': '蓝魔之泪',
        'info': '+100% 收集效果',
        'probability': 0.001,
    },
    {
        'id': 11,
        'name': '森林精华',
        'info': '+5% 合成概率',
        'probability': 0.38,
    },
]

#-----------------------------------------------------------------------------------
# 开始模拟
#-----------------------------------------------------------------------------------
drop_data = []

for item in range(drop_length):
    #-----------------------------------------------------------------------------------
    # 每次手机的时候有 20% 的概率掉落道具
    #-----------------------------------------------------------------------------------
    drop_random = random.randint(0, 9)
    if drop_random in [0, 1]:  #5级的经贸有20%的概率掉落道具
        props_random = random.randint(0, 999)
        if props_random == 0:  #汤姆的神杖
            drop_data.append(props_data[4]['name'])
            print('当前掉落：%s' % props_data[4]['name'])

        if props_random == 999:  #蓝魔之泪
            drop_data.append(props_data[10]['name'])
            print('当前掉落：%s' % props_data[10]['name'])

        if props_random >= 1 and props_random <= 60:  #逗猫器
            drop_data.append(props_data[0]['name'])
            print('当前掉落：%s' % props_data[0]['name'])

        if props_random >= 61 and props_random <= 90:  #捕鼠玩具
            drop_data.append(props_data[1]['name'])
            print('当前掉落：%s' % props_data[1]['name'])

        if props_random >= 91 and props_random <= 110:  #钓猫棒
            drop_data.append(props_data[2]['name'])
            print('当前掉落：%s' % props_data[2]['name'])

        if props_random >= 111 and props_random <= 119:  #逗猫法杖
            drop_data.append(props_data[3]['name'])
            print('当前掉落：%s' % props_data[3]['name'])

        if props_random >= 120 and props_random <= 499:  #合成加速卡
            drop_data.append(props_data[5]['name'])
            print('当前掉落：%s' % props_data[5]['name'])

        if props_random >= 500 and props_random <= 559:  #猫魂水晶
            drop_data.append(props_data[6]['name'])
            print('当前掉落：%s' % props_data[6]['name'])

        if props_random >= 560 and props_random <= 589:  #琥珀精华
            drop_data.append(props_data[7]['name'])
            print('当前掉落：%s' % props_data[7]['name'])

        if props_random >= 590 and props_random <= 609:  #魔法水晶
            drop_data.append(props_data[8]['name'])
            print('当前掉落：%s' % props_data[8]['name'])

        if props_random >= 610 and props_random <= 608:  #九尾猫之魂
            drop_data.append(props_data[9]['name'])
            print('当前掉落：%s' % props_data[9]['name'])

        if props_random >= 619 and props_random <= 998:  #森林精华
            drop_data.append(props_data[11]['name'])
            print('当前掉落：%s' % props_data[11]['name'])

    else:
        print('当前掉落: 空')

print('掉宝总数量：%d' % len(drop_data))
print('掉宝总概率：%s' % str(len(drop_data) / drop_length))
dict = {}
for item in drop_data:
    dict[item] = dict.get(item, 0) + 1
print(dict)

#! python3
# coding = utf-8

import Game#自己写的Game类
import time

m=input("modol:")

if m=="1":
    #构造Game类有如下可用参数：
    name = "play" # ! 游戏名，必填，无默认值
    
    is_show = 'normal'#显示模式，可填 mute（完全静默），little（只显示每轮结果）， normal（显示游戏过程必要的信息），full（显示游戏过程所有细节），默认 normal
    Player_names=["master1","master2","master3","你"] # 4元 列表，对应四个玩家名字，不填默认["player1","player2","player3","player4"]，如果不全剩下的默认，如果超出选择前四个
    AI_names = ['zx_AI(zrzr)','zx_AI(zrzr)','zx_AI(zrzr)','human']#4元 列表，对应四个玩家采用哪个AI，可选:'no_AI','zr_AI','zx_AI(zrzr)','zx_AI(zrno)','zx_AI(nozr)','zx_AI(nono)','human';默认全部"no_AI"
    debug = False#开启的话,也没有任何改变，以后可能会用到
    Rules={"放炮":True, "碰": True, "吃":False}#字典，规则设定，默认全部False（这样比较难和牌）

    game = Game.Game( name ,
                                      is_show = is_show ,
                                      Player_names = Player_names ,
                                      AI_names = AI_names ,
                                      debug = debug ,
                                      Rules = Rules )
    game.play(3)
    for p in game.players_list:
            print(p.name, "胜率:", p.win_n / game.game_round)

elif m == "2":
    game = Game.Game("测试", "little",AI_names=["zx_AI(zrzr)"]*4)
    start_t=time.time()
    game.play(1)
    end_t=time.time()
    print(end_t-start_t)
elif m=="3":
    game = Game.Game("测试2", "little",AI_names=["zx_AI(zrzr)"]*4)
    for i in range(0, 10):
        game.play(100)
        # game.players_dic["a"].AI.s1 -=0.5
        # game.players_dic["a"].AI.s2 -= 0.5
        # game.players_dic["a"].AI.s3 -= 0.5
        # game.players_dic["a"].AI.k1 += 0.5
        # game.players_dic["a"].AI.k2 += 0.5
        # game.players_dic["a"].AI.k3 += 0.5
        for p in game.players_list:
            print(p.AI_name, ":", p.win_n / game.game_round)

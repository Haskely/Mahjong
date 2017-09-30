#! python3
# coding = utf-8

import Game#自己写的Game类

m=input("modol:")

if m=="1":
    #构造Game类有如下可用参数：
    name = "play" # ! 游戏名，必填，无默认值
    
    is_show = 'full'#显示模式，可填 mute（完全静默），little（只显示每轮结果）， normal（显示游戏过程必要的信息），full（显示游戏过程所有细节），默认 normal
    Player_names=["master1","master2","master3","你"] # 4元 列表，对应四个玩家名字，不填默认["player1","player2","player3","player4"]，(如果不全剩下的默认，如果超出选择前四个)
    AI_names = ['zx_AI(zrzr)','zx_AI(zrzr)','zx_AI(zrzr)','human']#4元 列表，对应四个玩家采用哪个AI，可选:'no_AI','zr_AI','zx_AI(zrzr)','zx_AI(zrno)','zx_AI(nozr)','zx_AI(nono)','human'(human是手动玩）;默认全部"no_AI"
    debug = False#开启的话,会载入固定的初始牌以便于重现问题
    Rules={"放炮":True, "碰": True, "吃":False}#字典，规则设定，默认全部False（这样比较难和牌）,吃规则还没编

    game = Game.Game( name ,
                      is_show = is_show ,
                      Player_names = Player_names ,
                      AI_names = AI_names ,
                      debug = debug ,
                      Rules = Rules )#初始化游戏啦
    game.play(3)#玩3局
    game.print_win_rate()#打印胜率

elif m == "2":
    game = Game.Game("测试", "normal",AI_names=["zx_AI(zrzr)"]*3+["zx_AI(nozr)"],Rules={"放炮":True, "碰": True, "吃":False})
    game.play(10)
    print(game.time_count["whole_time"])
    game.print_win_rate()

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
        print(game.time_count[0])
        game.print_win_rate()

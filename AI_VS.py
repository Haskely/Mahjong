import Game
import time
from multiprocessing import Lock,Process

def write_output(output):
    with Lock():
        with open("output.txt","a+") as f:
            f.write(output)

def AI_VS(AI_name1,AI_name2,n):
    game = Game.Game("play","mute",Player_names=["张忆杭","齐洋","张瑞","张子新"],AI_names=[AI_name1]*3+[AI_name2], debug = False,Rules={"放炮":True, "碰": True, "吃":False})
    start_t=time.time()
    game.play(n)
    end_t=time.time()
    print("耗费时间:",end_t-start_t,"秒")
    output="[%s x3_vs_%s ] %d次测试：\n"%(AI_name1,AI_name2,n)
    for p in game.players_list:
        output += p.AI_name+":"+str(p.win_n / game.game_round)+"\n"
    write_output(output)
    # with open("output.txt", "a+") as f:
    #     f.write(output)
    print("胜率:",output)
    
if __name__ == "__main__":
    n=int(input("测试次数:"))
    vs_list=[["no_AI","zx_AI(zrzr)"],["no_AI","zx_AI(zrno)"],["no_AI","zx_AI(nozr)"],["no_AI","zx_AI(nono)"]]
    for arg in vs_list:
        Process(target = AI_VS, args=(arg[0],arg[1],n)).start()
    print ("process all started!")

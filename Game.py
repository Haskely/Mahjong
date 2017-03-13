from random import shuffle
from copy import deepcopy
import AI


class Game():
    globle_name_set=set()
    def __init__(self,name,is_show = 'normal',Player_names=["player1","player2","player3","player4"], AI_names = ['no_AI','no_AI','no_AI','no_AI'],debug = False ,Rules={"放炮":False, "碰": False, "吃":False}):
        if name in Game.globle_name_set:
            name = input("发现%s重名！请重新输入游戏名称:"%name)
        self.name=name
        self.debug = debug
        self.gametable= Gametable(debug)
        self.is_show=is_show#'mute','little','normal','full'
        if len(Player_names) <4:
            for i in range(len(Player_names),4):
                Player_names.append("player%d"%i)
        self.players_list=[Player(self.gametable,Rules,Player_names[0],AI_names[0],self.is_show),
                            Player(self.gametable,Rules,Player_names[1],AI_names[1],self.is_show),
                            Player(self.gametable,Rules,Player_names[2],AI_names[2],self.is_show),
                            Player(self.gametable,Rules,Player_names[3],AI_names[3],self.is_show)]
        self.Rules=Rules
        self.gamestate=0
        self.game_round = 0
        self.turn = 0
    def play(self,r):#开始游戏
        self.game_round = r
        #r=int(input("玩多少局?"))
        for p in self.players_list:
            p.win_n=0
        while(r>0):
            r-=1
            self.gametable.shuffle()#洗牌
            self.start()#发牌
            self.turn=1
            while(self.gamestate==1):#游戏中。。。
                if self.is_show in ['normal','full']:
                    print("\n\n第%d轮"%self.turn)
                self.turn+=1
                i=0
                while i<4 and (self.gamestate==1):
                    if self.players_list[i].draw(self.gametable):
                        if self.is_win(self.players_list[i]):
                            break
                        # if self.game_player_list[0].cnt[18]>2:
                        #     print("!")
                    else:
                        if self.is_show != 'mute':
                            print("平局")
                        self.gamestate = 3

                    self.players_list[i].drop(self.gametable)
                    for k in range(0, 4):
                        if self.players_list[k].pong(self.gametable):
                            if self.is_win(self.players_list[k]):
                                break
                            i = k
                            self.players_list[i].drop(self.gametable)
                    i += 1
            for p in self.players_list:#玩家归还牌
                p.reset()
            #print("end",self.turn)
        
    def start(self):#发牌
        for i in range(0, 13):
            for p in self.players_list:
                p.draw(self.gametable)
        self.gamestate=1

    def is_win(self,p):
        if p.hu_judge():
            self.winner = p.name
            self.gamestate = 2
            p.win_n += 1
            if self.is_show != 'mute':
                p.show("和牌")
                print("!!!胜利者是:", self.winner, "\n")
            return True
        return False

class Player():

    globle_name_list=['']

    def __init__(self,gametable,Rules,name = str(len(globle_name_list)),AI_name = None,is_show='normal'):
        self.gametable = gametable
        self.set_name(name)
        self.set_AI(AI_name)
        if is_show == 'little':
            is_show = 'mute'
        self.is_show = is_show
        self.reset()
        self.Rules=Rules
        self.win_n = 0
#初始化相关方法：
    def set_name(self,name):
        if name in Player.globle_name_list:
            name = input("发现%s名字已经存在！请重新输入玩家名称:"%name)
        self.name=name
        Player.globle_name_list.append(name)

    def set_AI(self,AI_name):
        self.AI_name = AI_name
        self.AI = AI.init(self,self.gametable)

    def reset(self):
        self.cnt = [0] * 34  # 0-8:"万";9-17:"条";18-26:"桶";27-33:"东","南","西","北","白","发","中"
        self.cnt_p = [0] * 34
        self.last_draw = None
        self.peng = 0
        self.state = True
##


#显示相关方法：
    def show(self,type,tile = -1):
        if self.is_show == 'mute':
            pass
        elif self.is_show == 'normal':
            if type == '摸牌':
                print(self.name, ":", type,  end=" ")
            elif type == '出牌':
                print(self.name,":", type, self.get_tile_name(tile), end="\n")
            elif type == '和牌':
                print(self.name,":我和牌了!")
                self.show_tiles()
            else:
                print("操作类型有误")
        elif self.is_show == 'full':
            print(self.name, type, self.get_tile_name(tile))
            self.show_tiles()
        else:
            print("显示模式有误,应该为mute,normal 或 full")

    def show_tiles(self):
        print("玩家:",self.name,"->")
        for i in range(0, 3):
            for j in range(0, 9):
                e = self.cnt[i*9+j]
                while(e):
                    print("%d"%(j+1) + Gametable.type[i],end=' ')
                    e-=1
                    #print(e)
                    if e<0:
                        print("!")
        for j in range(0,7):
            e=self.cnt[27+j]
            while(e):
                print(Gametable.s_type[j] , end=' ')
                e -= 1
        print("\n")
##

#游戏行为相关方法：
    def draw(self,gametable = None):
        if gametable == None:
            gametable = self.gametable

        t=gametable.draw()

        if t!="End":
            # if t == 18:
            #     print("!")
            # if self.name=="a" and t == 8:
            #     print("!")
            self.cnt[t]+=1
            self.last_draw=t

            # if self.cnt[18]>4:
            #     print("!")
            self.show("摸牌",t)

            return True
        elif t=="End":
            return False

    def drop(self,gametable  = None):
        if gametable == None:
            gametable = self.gametable
        t=self.AI.think()
        # if self.cnt[t]<=0:
        #     print("!")
        if t==None:
            print(t)
        self.cnt[t] -= 1
        gametable._receive(self.name,t)
        self.show("出牌", t)

    def pong(self,gametable = None):
        if gametable == None:
            gametable = self.gametable

        if self.Rules["放炮"]:
            self.cnt[gametable.receive_tiles[-1][1]] += 1
            if self.hu_judge():
                if self.is_show in ["normal", "full"]:
                    print(gametable.receive_tiles[-1][0],"放炮给",self.name,gametable.receive_tiles[-1][1],sep=" ")
                return True
            self.cnt[gametable.receive_tiles[-1][1]] -= 1

        if self.Rules["碰"]:
            if self.cnt[gametable.receive_tiles[-1][1]]==2:

                self.cnt[gametable.receive_tiles[-1][1]] += 1
                if self.hu_judge():
                    return False
                self.cnt[gametable.receive_tiles[-1][1]] -= 1

                if self.AI.think_peng():
                    self.cnt_p[gametable.receive_tiles[-1][1]]+=1
                    self.cnt[gametable.receive_tiles[-1][1]] -= 2
                    self.peng +=1
                    if self.is_show in ["normal","full"]:
                        print("\n",self.name,"碰了",gametable.receive_tiles[-1][0],"的",self.get_tile_name(gametable.receive_tiles[-1][1]))
                        return True
        if self.Rules["吃"]:
            pass

        return False

        pass


    def hu_judge(self):
        tmp = deepcopy(self.cnt)
        for t in range(0,34):
            if (tmp[t] >= 2):
                tmp[t] -= 2
                #34
                ret = 0
                for i in range(0, 19, 9):
                    for j in range(0, 9):
                        if (tmp[i + j] >= 3):
                            tmp[i + j] -= 3
                            ret += 1
                        while (j + 2 < 9 and tmp[i + j] and tmp[i + j + 1] and tmp[i + j + 2]):
                            tmp[i + j] -= 1
                            tmp[i + j + 1] -= 1
                            tmp[i + j + 2] -= 1
                            ret += 1
                for j in range(0, 7):
                    if (tmp[27 + j] >= 3):
                        tmp[27 + j] -= 3
                        ret += 1

                tmp[t] += 2
                if (ret+self.peng == 4):
                    return True
        return False
##


#其他方法：
    def get_tile_name(self, t):
        if t >= 0:
            if t <= 26:
                return str(t % 9 + 1) + Gametable.type[t // 9]
            elif t <= 33:
                return Gametable.s_type[t - 27]
        return ''

class Gametable():
    type = ["万", "条", "桶"]
    s_type = ["东", "南", "西", "北", "白", "发", "中"]

    def __init__(self,debug = False):
        self.Tiles=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
        #数字对应牌型0-8:"万";9-17:"条";18-26:"桶";27-33:"东","南","西","北","白","发","中"
        #self.shuffle()#洗牌
        self.debug=debug


    def shuffle(self):
        self.draw_loc = 0
        self.receive_cnt = [0] * 34
        self.receive_tiles = []
        if self.debug:
            self.Tiles=[25, 26, 22, 28, 24, 14, 12, 16, 12, 13, 20, 2, 26, 30, 17, 33, 9, 22, 31, 33, 27, 19, 25, 20, 11, 2, 22, 20, 25, 4, 32, 4, 16, 28, 19, 5, 24, 29, 26, 7, 20, 15, 0, 24, 9, 11, 25, 15, 2, 27, 30, 22, 31, 18, 6, 4, 29, 16, 14, 3, 9, 21, 3, 21, 8, 17, 1, 13, 29, 11, 18, 2, 23, 32, 10, 31, 1, 7, 12, 15, 19, 6, 14, 17, 4, 28, 32, 23, 1, 17, 14, 33, 27, 5, 8, 10, 18, 13, 21, 8, 30, 1, 26, 28, 0, 7, 3, 5, 21, 30, 12, 8, 5, 7, 10, 15, 9, 10, 13, 31, 19, 6, 23, 29, 18, 23, 32, 27, 0, 6, 3, 24, 33, 11, 0, 16]
        else:
            shuffle(self.Tiles)
    def draw(self):
        if self.draw_loc>=136:
            return "End"
        t=self.Tiles[self.draw_loc]
        self.draw_loc+=1
        # if t==18:
        #     print("!")
        return t

    def _receive(self,p_name,t):
        self.receive_tiles.append([p_name,t])
        self.receive_cnt[t] += 1

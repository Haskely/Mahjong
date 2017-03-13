AI_name_list=['no_AI','zr_AI','zx_AI(zrzr)','zx_AI(zrno)','zx_AI(nozr)','zx_AI(nono)','human']

def init(player,gametable):
    if player.AI_name == None:
        player.AI_name = player.name
    while player.AI_name not in AI_name_list:
        print("可用的AI方法有:", ", ".join(AI_name_list))
        player.AI_name = str(input("没有名为%s的AI,请指定正确的AI方法:"))
    if player.AI_name == 'no_AI':
        return no_AI(player,gametable)
    elif player.AI_name == 'zr_AI':
        return zr_AI(player,gametable)
    elif player.AI_name == 'zx_AI(zrzr)':
        return zx_AI(player,gametable,"zr_AI","zr_AI")#first 4 peng , second 4 drop
    elif player.AI_name == 'zx_AI(zrno)':
        return zx_AI(player,gametable,"zr_AI","no_AI")
    elif player.AI_name == 'zx_AI(nozr)':
        return zx_AI(player,gametable,"no_AI","zr_AI")
    elif player.AI_name == 'zx_AI(nono)':
        return zx_AI(player,gametable,"no_AI","no_AI")
    elif player.AI_name == 'human':
        return human(player,gametable)
    else:
        print("没有%s这个AI方法"%player.AI_name)
        return None

class human():
    def __init__(self,player,gametable):
        self.name='no_AI'
        self.player = player
        self.gametable = gametable


    def think_peng(self):
        self.Print_tiles()
        print("\n你可以碰牌: ",self.player.cnt[self.gametable.receive_tiles[-1][1]],"\n你要碰吗？(1要,2不要)")
        ans=input()
        if ans =="1":
            return True
        elif ans == "2":
            return False

    def Print_tiles(self):
        print("\n\n你当前有牌:")
        T_list = [None]*14
        k=0
        for i in range(0,34):
            e= self.player.cnt[i]
            if e:
                t_name=self.player.get_tile_name(i)
                while(e>0):
                    T_list[k]=i
                    print(t_name, end="\t")
                    k += 1
                    e -= 1
        print()
        return k,T_list


    def think(self):
        print("\n\n你摸到的牌:",self.player.get_tile_name(self.player.last_draw))
        print("\n桌面上已出去的牌:")
        for t in range(0,34):
            if self.gametable.receive_cnt[t]:
                print(self.player.get_tile_name(t),"x",self.gametable.receive_cnt[t],end="\t")


        k,T_list = self.Print_tiles()
        
        for i in range(1,k+1):
            print(i,end="\t")
        while 1:
            print("\n\n输入要出的牌编号:")
            try:
                o=int(input())
                if o in range(1,k+1):
                    return T_list[o-1]
            except:
                print("编号有误请重新输入")

class no_AI():
    def __init__(self,player,gametable):
        self.name='no_AI'
        self.player = player
        self.gametable = gametable

    def think_peng(self):
        return True

    def think(self,player = None):
        if player == None:
            player = self.player
        t = player.last_draw
        for i in range(0, 3):
            for j in range(1, 8):
                k = i * 9 + j
                if player.cnt[k] == 1:
                    if player.cnt[k - 1] + player.cnt[k + 1] == 0:
                        t = k
                        return t
                    elif player.cnt[k - 1] + player.cnt[k + 1] == 1:
                        t = k
                # 0
                k = i * 9 + 0
                if player.cnt[k] == 1:
                    if player.cnt[k + 1] == 0:
                        t = k
                    elif player.cnt[k + 1] == 1:
                        t = k
                # 1
                k = i * 9 + 8
                if player.cnt[k] == 1:
                    if player.cnt[k - 1] == 0:
                        t = k
                    elif player.cnt[k - 1] == 1:
                        t = k
        for k in range(0, 7):
            if player.cnt[k + 27] == 1:
                t = k + 27
                return t
        return t

class zr_AI():
    def __init__(self,player,gametable,s0=10,s1=6,s2=6,k0=2,k1=1,k2=1):
        self.name='zr_AI'
        self.player = player
        self.gametable = gametable
        self.s0 = s0
        self.s1 = s1
        self.s2 = s2
        self.k0 = k0
        self.k1 = k1
        self.k2 = k2

    def get_num_t(self,t):
        return 4-self.player.cnt[t]-self.gametable.receive_cnt[t]#改进空间为计算其他玩家持牌的概率？？？

    def get_first_level_ts(self,t):
        ts=set()
        p=t%9
        if t>=0:
            if t<=26:
                p = t % 9
                if p*(p-8):
                    return [t+1,t-1]
                else:
                    return [t+1-1*p//4]
            elif t<=33:
                return []
        return None

    def get_second_level_ts(self,t):
        ts=set()
        p=t%9
        if t>=0:
            if t<=26:
                p = t % 9
                if p*(p-8)*(p-1)*(p-7):
                    return [t+2,t-2]
                else:
                    return [t+(p*p*p-12*p*p+11*p)//42+2]
            elif t<=33:
                return []
        return None

    def think_peng(self):
        l_r_t=self.player.cnt[self.gametable.receive_tiles[-1][1]]
        sum_rp,sum_rpp = 0,0
        for t in range(0,34):
            sum_rp += self.rp_t(t)
        self.player.cnt[l_r_t] -= 2
        for t in range(0,34):
            sum_rpp += self.rp_t(t)
        sum_rpp += 3 * self.s0
        self.player.cnt[l_r_t] += 2

        return (sum_rpp>=sum_rp)

    def think(self,player = None,gametable = None):
        if player == None:
            player = self.player
        if gametable == None:
            gametable = self.gametable

        min_p=16*(self.s0+self.s1*self.s2+self.k0+self.k1*self.k2)
        drop_t=None
        for t in range(0,34):
            p_t=self.rp_t(t)
            if p_t!=0 and p_t<=min_p:
                min_p=p_t
                drop_t=t
        if drop_t == None:
            print("?")
        return drop_t

    def rp_t(self,t):
        p_t = 0
        sn_0 = self.player.cnt[t]
        if sn_0:
            sn_1, sn_2, kn_0, kn_1, kn_2 = 0, 0, 0, 0, 0
            kn_0 = self.get_num_t(t)
            for t1 in self.get_first_level_ts(t):
                sn_1 += self.player.cnt[t1]
                kn_1 += self.get_num_t(t1)
            for t2 in self.get_second_level_ts(t):
                sn_2 += self.player.cnt[t2]
                kn_2 += self.get_num_t(t2)
            p_t = sn_0 * self.s0 + (sn_1 * self.s1) + (sn_2 * self.s2) + kn_0 * self.k0 + (kn_1 * self.k1) + (kn_2 * self.k2)
        return p_t

class zx_AI(zr_AI,no_AI):
    def __init__(self,player,gametable,peng,drop):
        zr_AI.__init__(self,player,gametable)
        no_AI.__init__(self,player,gametable)
        self.name='zx_AI'
        self.AI4peng=peng
        self.AI4drop=drop
        # self.player = player
        # self.gametable = gametable
        self.n=1
    def get_p_Ts(self,Ts):
        p=0
        for t in Ts:
            n = (4-self.player.cnt[t]-self.gametable.receive_cnt[t])
            p += n/122
        return p


    def think_peng(self):
        l_r_t = self.player.cnt[self.gametable.receive_tiles[-1][1]]
        max_n=self.n
        n = 0
        while n <= max_n:
            p = self.get_p_Ts(self.get_n_ava_t(n))
            if p > 0:
                self.player.cnt[l_r_t] -= 2
                self.player.peng += 1
                pp = self.get_p_Ts(self.get_n_ava_t(n))
                self.player.cnt[l_r_t] += 2
                self.player.peng -= 1
                if self.player.is_show in ["normal", "full"]:
                    print("神级判碰")
                return pp>=p
            n += 1

        if self.AI4peng == "zr_AI":
            return zr_AI.think_peng(self)
        elif self.AI4peng == "no_AI":
            return no_AI.think_peng(self)
        else:
            print ("AI4peng not found!")

    def think(self):
        t_best=self.get_best_drop_t(self.n)
        if t_best !=None:
            return t_best

        if self.AI4drop == "zr_AI":
            return zr_AI.think(self,self.player,self.gametable)
        elif self.AI4drop == "no_AI":
            return no_AI.think(self,self.player)
        else:
            print ("AI4drop not found!")


    def get_best_drop_t(self,max_n):
        n=0
        while n<=max_n:
            p_max,t_best=self.get_n_drop_t(n)
            if p_max != 0:
                if self.player.is_show in ["normal","full"]:
                    print("雀神在此！%d级听牌!"%n,end=" ")
                return t_best
            n += 1

        return None


    def get_n_drop_t(self,n):
        n=int(n)
        p_max = 0
        for t in range(0, 34):
            if self.player.cnt[t]>0:
                self.player.cnt[t] -= 1
                Tx = self.get_n_ava_t(n)
                p_x=self.get_p_Ts(Tx)
                if p_x>=p_max:
                    p_max=p_x
                    t_best=t
                self.player.cnt[t] += 1
        return p_max,t_best

    def get_n_ava_t(self,n):
        if n == 0:
            T0 = []
            T0p = []
            for t in range(0, 34):
                self.player.cnt[t] += 1
                if self.player.hu_judge():
                    T0.append(t)
                self.player.cnt[t] -= 1
            return T0
        elif n>=1:
            T0 = self.get_n_ava_t(n-1)
            p0 = self.get_p_Ts(T0)
            T1 = []
            T1p = []
            for t in range(0, 34):
                self.player.cnt[t] += 1
                T0x = self.get_n_ava_t(n-1)
                p0x = self.get_p_Ts(T0x)
                if p0x > p0:
                    T1.append(t)
                self.player.cnt[t] -= 1
            return T1
        else:
            print("n应该为正整数")
    # def get_zero_avalible_t(self,d_t):
    #     T0=[]
    #     T0p=[]
    #     for t in range(0,34) and t!=d_t:
    #         self.player.cnt[t] +=1
    #         if self.player.hu_jugde():
    #             T0.append(t)
    #         self.player.cnt[t] -= 1
    #     return T0
    #
    # def get_first_avalible_t(self,d_t):
    #     T0=self.get_zero_avalible_t()
    #     p0=get_p_Ts(T0)
    #     T1=[]
    #     T1p=[]
    #     for t in range(0,34) and t != d_t:
    #         self.player.cnt[t] +=1
    #         T0x = self.get_zero_avalible_t()
    #         p0x=get_p_Ts(T0x)
    #         if p0x > p0:
    #             T1.append(t)
    #             T1p.append(p0x)
    #         self.player.cnt[t] -= 1
    #     return T1,T1p
    #
    # def get_second_avalible_t(self):
    #     T1,T1p=self.get_first_avalible_t()
    #     p1=get_p_Ts(T1)
    #     T2=[]
    #     T2p=[]
    #     for t in range(0,33):
    #         self.player.cnt[t] +=1
    #         T1x = self.get_first_avalible_t()
    #         p1x=get_p_Ts(T1x)
    #         if p1x > p1:
    #             T2.append(t)
    #             T2p.append(p1x)
    #         self.player.cnt[t] -= 1
    #     return T2,T2p


    def no_ai(self,player = None):
        if player == None:
            player = self.player
        t = player.last_draw
        for i in range(0, 3):
            for j in range(1, 8):
                k = i * 9 + j
                if player.cnt[k] == 1:
                    if player.cnt[k - 1] + player.cnt[k + 1] == 0:
                        t = k
                        return t
                    elif player.cnt[k - 1] + player.cnt[k + 1] == 1:
                        t = k
                # 0
                k = i * 9 + 0
                if player.cnt[k] == 1:
                    if player.cnt[k + 1] == 0:
                        t = k
                    elif player.cnt[k + 1] == 1:
                        t = k
                # 1
                k = i * 9 + 8
                if player.cnt[k] == 1:
                    if player.cnt[k - 1] == 0:
                        t = k
                    elif player.cnt[k - 1] == 1:
                        t = k
        for k in range(0, 7):
            if player.cnt[k + 27] == 1:
                t = k + 27
                return t
        return t

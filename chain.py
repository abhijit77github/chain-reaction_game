import sys
sys.setrecursionlimit(10000)

class element:

    def __init__(self):
        self.cnt = 0
        self.col = None
        self.nbr = None


plr = ['a', 'b', 'c', 'd']


class Chain:

    def __init__(self):
        h, w = 6, 5
        self.h = h
        self.w = w
        self.box = [[element() for i in range(w)] for j in range(h)]
        self.vallid_plr = []  # no. of players joined the game
        self.crnt_plrs = []  # no. of player vallid to get a turn
        # self.plrs=self.plr_lst(no_of_plr)
        self.plrs = []
        self.crnt_plr_indx = 0
        # self.points_lst=[0 for i in range(no_of_plr)]
        self.move_cnt = 0
        self.checked = False
        self.terminated = False
        self.started = False
        self.result = None

    # function to handle if the number of player joined is less than in
    # it will be handled in game manager

    def start(self, no_of_plr):
        self.plrs = self.plr_lst(no_of_plr)

    def plr_lst(self, no_of_plr):
        if no_of_plr <= len(plr):
            plrs = []
            for i in range(no_of_plr):
                plrs.append(i)
            # self.vallid_plr.append("True")
            self.crnt_plrs = plrs
            self.vallid_plr = plrs
            self.add_nbr()
            #print(self.crnt_plrs)
            return plrs

    def get_nbr(self, pos):
        negh = []
        if pos[0] - 1 >= 0:
            negh.append((pos[0] - 1, pos[1]))
        if pos[0] + 1 < self.h:
            negh.append((pos[0] + 1, pos[1]))
        if pos[1] - 1 >= 0:
            negh.append((pos[0], pos[1] - 1))
        if pos[1] + 1 < self.w:
            negh.append((pos[0], pos[1] + 1))
        return negh

    def add_nbr(self):
        for i in range(self.h):
            for j in  range(self.w):
                self.box[i][j].nbr= self.get_nbr([i,j])

    def pos_is_vallid(self, plr_index, pos):
        if self.box[pos[0]][pos[1]].col == self.vallid_plr[plr_index] or self.box[pos[0]][pos[1]].col is None:
            return True
        else:
            return False

    # returns the player index from col value
    def get_plr_index(self, col):
        for i in range(len(self.plrs)):
            if self.plrs[i] == col:
                return i

    def move(self, plr_index, pos):
        self.move_cnt = self.move_cnt + 1
        if self.move_cnt > len(self.plrs):
            self.checked = True
        p = self.box[pos[0]][pos[1]].cnt = self.box[pos[0]][pos[1]].cnt + 1
        self.box[pos[0]][pos[1]].col = self.plrs[plr_index]
        # here we might need to change the coler of the starting
        # position also
        """
        if p >= len(self.get_nbr(pos)):
            print(f'brust shoud be hre {pos[0]}, {pos[1]} has  {len(self.get_nbr(pos))} neighbor..')
            self.box[pos[0]][pos[1]].col = None
            self.box[pos[0]][pos[1]].cnt = 0
            for i in self.get_nbr(pos):
                self.box[i[0]][i[1]].col = self.vallid_plr[plr_index]
                self.move(plr_index, (i[0], i[1]))
        
        #2nd approch
        nbr=self.get_nbr(pos)
        if p >= len(nbr):
            print(f'brust shoud be hre {pos[0]}, {pos[1]} has  {len(nbr)} neighbor..')
            self.box[pos[0]][pos[1]].col = None
            self.box[pos[0]][pos[1]].cnt = 0
            for node in nbr:
                self.box[node[0]][node[1]].col=plr_index
                self.box[node[0]][node[1]].cnt +=1
            self.brust(plr_index,self.get_nbr(pos),0)
        
        #3rd approch
        if p >= len(self.get_nbr(pos)):
            self.overflow(plr_index,pos)
        """
        #4th approch
        if p>= len(self.box[pos[0]][pos[1]].nbr):
            flag = False
            cnt = 0
            nbr = self.box[pos[0]][pos[1]].nbr
            self.box[pos[0]][pos[1]].col = None
            self.box[pos[0]][pos[1]].cnt = 0
            while not flag:
                flag = True
                new_nbr = []
                for i in nbr:
                    self.box[i[0]][i[1]].col = plr_index
                    self.box[i[0]][i[1]].cnt += 1
                    if self.box[i[0]][i[1]].cnt >= len(self.box[i[0]][i[1]].nbr):
                        flag = False
                        self.box[i[0]][i[1]].col = None
                        self.box[i[0]][i[1]].cnt = 0
                        for j in self.box[i[0]][i[1]].nbr:
                            new_nbr.append(j)


                nbr = new_nbr
                cnt += 1
            #print(f" while loop ran : {cnt} times")
            #print("move executed")


    def overflow(self,plr_index,pos):
        self.box[pos[0]][pos[1]].col=None
        self.box[pos[0]][pos[1]].cnt= 0
        for i in self.get_nbr(pos):
            self.box[i[0]][i[1]].col= plr_index
            self.box[i[0]][i[1]].cnt += 1
            if self.box[i[0]][i[1]].cnt >= len(self.get_nbr(i)):
                self.overflow(plr_index,i)

    def brust(self,plr_index,nodes,rec_cnt):
        brst_pnt=[]
        for i in nodes:
            cnt=len(self.get_nbr(i))
            if self.box[i[0]][i[1]].cnt >= cnt:
                self.box[i[0]][i[1]].col=None
                self.box[i[0]][i[1]].cnt=0
                brst_pnt.append(i)
        nbr_lst=[]
        if len(brst_pnt):
            for j in brst_pnt:
                p=self.get_nbr(j)
                for l in p:
                    nbr_lst.append(l)
            if len(nbr_lst):
                for k in nbr_lst:
                    self.box[k[0]][k[1]].cnt +=1
                    self.box[k[0]][k[1]].col = plr_index
                self.brust(plr_index,nbr_lst,(rec_cnt +1))
        #print(rec_cnt)
        return rec_cnt

    def next_turn(self, crnt_plr_index):
        if crnt_plr_index + 1 > len(self.vallid_plr) - 1:
            p = 0

        else:
            p = crnt_plr_index + 1
        #print(p)
        #print(self.crnt_plrs)
        if p in self.crnt_plrs:
            return p
        else:
            #print("recursion should be called")
            return self.next_turn(p)

    def play(self, plr_index, pos):
        if self.pos_is_vallid(plr_index, pos):
            self.move(plr_index, pos)
            if self.is_game_ended():
                # provide game result
                #print("game ended")
                self.terminated = True
            else:
                next = self.next_turn(plr_index)
                self.crnt_plr_indx = next
                #print(f'next returned {self.crnt_plr_indx}')
                return next
        else:
            return self.crnt_plr_indx
        # send msg to next player for ther turn
        # which will in turn play again

    def is_game_ended(self):
        col_lst = []
        for i in range(self.h):
            for j in range(self.w):
                if (self.box[i][j].col not in col_lst) and self.box[i][j].col != None:
                    col_lst.append(self.box[i][j].col)
        if self.checked:
            self.crnt_plrs = col_lst
            self.crnt_plrs.sort()
        if (len(col_lst) == 1) and self.checked == True:
            #print(f"game ended --------winner is {col_lst[0]}")
            self.result=col_lst[0]
            return True
        else:
            return False
        """
		cnt=0
		plr_index=None
		for i in range(len(self.plrs)):
			if(self.vallid_plr[i]==True):
				cnt=cnt+1
		if(cnt==1):
			print("game ended --------")
			for i in range(len(self.vallid_plr)):
				if(self.vallid_plr[i]==True):
					print(f' The winner is player {self.plrs[i]}')
	    


def print_box(game):
    for i in range(game.h):
        print("|| ", end="")
        for j in range(game.w):
            print(f' {game.box[i][j].col},{game.box[i][j].cnt}  || ', end="")
        print("")


def main():
    num_of_plr = 2
    game = Chain()
    game.start(3)
    #print_box(game)
    for i in range(6):
        for j in range(5):
            print("\n"+f" position {i},{j} has :")
            print(game.get_nbr([i,j]))
            print("\n")
   
    plr_index = 0
    flag = True

    while (flag != False):

        row = int(input(f"enter {game.crnt_plr_indx}  player pos row:"))
        col = int(input("col :"))
        n_p = game.play(plr_index, (row, col))
        if game.terminated == True:
            flag = False
        else:
            plr_index = n_p
        print_box(game)
"""
#main()
#print(sys.getrecursionlimit())
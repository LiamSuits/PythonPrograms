class Minimax:
    def __init__(self, nimState, minMaxLevel):
        self.state = nimState
        self.level = minMaxLevel
        self.child = []
        
    def split_single(self,num):
        pairs = []
        i = 1
        flag = True
        while flag:
            big_half = num - i
            if big_half <= i:
                flag = False
            else:
                pairs.append([i,big_half])
                i = i + 1
        return pairs    
        
    def split(self):
        possibs = []
        for index in range(len(self.state)):
            if self.state[index] > 2:
                for split in self.split_single(self.state[index]):
                    temp = list(self.state)
                    temp[index] = split.pop(0)
                    for num in split:
                        temp.insert(index+1, num)
                    possibs.append(temp)
        # remove duplicate possibilities
        if possibs == []:
            no_dupes = self.state
        else:
            for chunk in possibs:
                chunk.sort()
                no_dupes = []
            for chunk in possibs:
                if not chunk in no_dupes:
                    no_dupes.append(chunk)
        return(no_dupes)
    
    def add_child(self,new_child):
        self.child.append(new_child)
        
    def build(self):
        possibs = self.split()
        if self.state != possibs:    
            for outcome in possibs:
                outcome.sort()
                if self.level == 'MAX':
                    state = 'MIN'
                else:
                    state = 'MAX'
                new_child = Minimax(outcome,state)
                self.add_child(new_child)
                new_child.build()
                
    def print_tree(self, indent, last):
        print(indent,end='')
        if last:
            print('\-',end='')
            indent = indent + "  "
        else:
            print('+ ',end='')
            indent += "| "
        print(self.state,end='')
        if last:
            print(' ' + self.level)
        else:
            print('')
        for child in self.child:
            last = False
            if self.child[len(self.child)-1] == child:
                last = True
            child.print_tree(indent, last)
                  

pile = 0
while pile < 3:
    try:
        pile = int(input('Choose your initial size of the pile. Should be more than 2: '))
    except:
        pass
root = Minimax([pile],'MAX')
root.build()
root.print_tree('',True)
                

    


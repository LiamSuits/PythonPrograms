class CircularQueue:
    def __init__(self, capacity):
        if type(capacity) != int or capacity<=0:
            raise Exception('Capacity Error')
        self.__items = []
        self.__capacity = capacity
        self.__count = 0
        self.__head = 0
        self.__tail = 0
        
    def enqueue(self, item):
        if self.__count == self.__capacity:
            raise Exception('Error: Queue is full')
        if len(self.__items) < self.__capacity:
            self.__items.append(item)
        else:
            self.__items[self.__tail]=item
        self.__count += 1
        self.__tail=(self.__tail +1) % self.__capacity
        
    def dequeue(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        item= self.__items[self.__head]
        self.__items[self.__head]=None
        self.__count -=1
        self.__head=(self.__head+1) % self.__capacity
        return item    
    
    def peek(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        return self.__items[self.__head]    
    
    def isEmpty(self):
        return self.__count == 0 
    
    def isFull(self):
        return self.__count == self.__capacity    
    
    def size(self):
        return self.__count   
    
    def capacity(self):
        return self.__capacity   
    
    def clear(self):
        self.__items = []
        self.__count=0
        self.__head=0
        self.__tail=0   
        
    def __str__(self):
        str_exp = "]"
        i=self.__head
        for j in range(self.__count):
            str_exp += str(self.__items[i]) + " "
            i=(i+1) % self.__capacity
        return str_exp + "]"
    
    def __repr__(self):
        return str(self.__items) + ' Head =' + str(self.__head) + ' Tail ='+str(self.__tail) + ' ('+str(self.__count)+'/'+str(self.__capacity)+')'
    
class OnTable:
    def __init__(self):
        self.__cards = []
        self.__faceUp = []
        
    def place(self,player,card,hidden):
        if player == 1:
            self.__cards.insert(0,card)
            self.__faceUp.insert(0,hidden)
        else:
            self.__cards.append(card)
            self.__faceUp.append(hidden)
        
    def cleanTable(self):
        return_cards = self.__cards
        self.__cards = []
        self.__faceUp = []
        return return_cards
        
    def __str__(self):
        card_list = []
        for index in range(len(self.__cards)):
            if self.__faceUp[index] == False:
                card_list.append(self.__cards[index])
            else:
                card_list.append('XX')
                
        return str(card_list)
    
def compare(card1, card2):
    val1 = ranks.index(card1[0])
    val2 = ranks.index(card2[0])
    if val1 > val2:
        return 1
    elif val1 < val2:
        return -1
    else:
        return 0
    
input_file = "shuffledDeck.txt"
try:
    deck = open(input_file,'r').read().splitlines()
except FileNotFoundError:
    raise Exception('Error: The file does not exist')
# check for not correct deck size
assert len(deck) == 52, 'Error: The deck does not have 52 cards'

for card in deck:
    card = card.upper()

suits=['D', 'C', 'H', 'S']
ranks=['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
cards=[]
for rank in ranks:
    for suit in suits:
        cards.append(rank+suit)
all_cards = True
for card in cards:
    if not card in deck:
        all_cards = False
assert all_cards == True, 'Error: The deck does contain the correct cards'

player_1 = CircularQueue(52)
player_2 = CircularQueue(52)

while len(deck) != 0:
    player_1.enqueue(deck.pop())
    player_2.enqueue(deck.pop())
    
valid = False
amounts = ['1', '2', '3']
while not valid:
    war_amount = input('Would you like to play a War with 1, 2, or 3 cards face down?: ')
    if war_amount in amounts:
        valid = True
        war_amount = int(war_amount)
    else:
        print('That is not a valid input. Enter a number between 1 and 3.')
        
game_over = False
table = OnTable()

while not game_over:
    if player_1.size() == 0 or player_2.size() == 0:
        if player_1.size() == 0:
            for card in table.cleanTable():
                player_2.enqueue(card)        
        elif player_2.size() == 0:
            for card in table.cleanTable():
                player_1.enqueue(card)                   
        game_over = True
    else:
        faceup1 = player_1.dequeue()
        table.place(1, faceup1, False)
        faceup2 = player_2.dequeue()
        table.place(2, faceup2, False)
        input(table)
        if compare(faceup1,faceup2) == 1:
            for card in table.cleanTable():
                player_1.enqueue(card)
        elif compare(faceup1,faceup2) == -1:
            for card in table.cleanTable():
                player_2.enqueue(card)
        else:
            for num in range(war_amount):
                if player_1.size() == 0:
                    for card in table.cleanTable():
                        player_2.enqueue(card)                
                    game_over = True
                else:
                    table.place(1, player_1.dequeue(), True)
                
                if player_2.size() == 0:
                    for card in table.cleanTable():
                        player_1.enqueue(card)                
                    game_over = True
                else:
                    table.place(2, player_2.dequeue(), True)            
                    
        print('Player 1: ' + str(player_1.size()) + ' cards' + '\n' + 'Player 2: ' + str(player_2.size()) + ' cards')
        
if player_1.size() > player_2.size():
    print('Player 1 wins!')
else:
    print('Player 2 wins!')

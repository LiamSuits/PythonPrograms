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
            str_exp += str(self.__items[i]) + ','
            i=(i+1) % self.__capacity
        return str_exp + "]"    
    
reg = CircularQueue(3)
vip = CircularQueue(3)
exit = False
while not exit:
    action = input('Add, Serve, or Exit:').lower()
    if action == 'add':
        name = input('Enter the name of the person to add:')
        is_vip = 'true' == input('Is the customer VIP?').lower()
        if is_vip:
            try:
                vip.enqueue(name)
                print('add ' + name + ' to VIP line.')
            except:
                print('Error: VIP customers queue is full')
        else:
            try:
                reg.enqueue(name)
                print('add ' + name + ' to line.')
            except:
                print('Error: Normal customers queue is full')
                
    if action == 'serve':
        try:
            if not vip.isEmpty():
                served = vip.dequeue()
            else:
                served = reg.dequeue()
            print(served + ' has been served')
        except:
            print('Error: Both queues are empty')
    if action == 'exit':
        exit = True
        print('Qutting')
    else:
        print('people in the line: ' + str(reg))
        print('VIP customers queue: ' + str(vip))
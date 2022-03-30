class Stack:
    def __init__(self):
        self.top=[]
        
    def __str__(self):
        return str(self.top[::1])

    def push(self,data):
        return self.top.append(data)
    
    def pop(self):
        if self.isEmpty():
            return print('stack is empty')
        return self.top.pop()

    def clear(self):
        self.top=[]

    def peek(self):
        if not self.isEmpty():
            return print(self.top[-1])
        return print('The data does not exist')

    def isEmpty(self):
        return len(self.top) == 0

    def size(self):
        if self.isEmpty():
            return print('stack is empty')
        return print("size : %d"%len(self.top))
    
    

#test
s = Stack()
s.size()
s.push(1)
s.pop()
s.push(2)
s.push(3)
s.peek()
print(s)
s.clear()
s.size()
s.peek()


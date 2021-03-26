class myStack:
    def __init__(self,number):
        self.number = number
    
    def myPush(self):
        a =[1,2]
        for i in a:
            self.number = i
            print(i)



data = myStack(2)
data.myPush()
        
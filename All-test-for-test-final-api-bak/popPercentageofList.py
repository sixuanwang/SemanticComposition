l = [0,1,2,3,4,5,6,7,8]

per2Remove = 0.4
num2Remove = int(len(l)*per2Remove)

for i in range(0,num2Remove):
	del l[-1]
	
print l
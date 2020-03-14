#Saving to text file


# Open function to open the file "MyFile1.txt"  
# (same directory) in append mode and 
file1 = open("MyFile.txt","w")

#example of how to print with formating
for x in range(1, 11):
    file1.write("{0:2d} {1:3d} \n". format(x, x+x))
    #file1.write('\n')

#closing file
file1.close()

#open in read mode
file1 = open("MyFile.txt", 'r')
print ("Output of Readlines after writing")
print (file1.readlines())
print ()
file1.close()

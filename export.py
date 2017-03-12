def process():
    fptr = open('part0.txt')
    out = open('result.html','w')
    line = fptr.readline()
    while line:
        out.writelines(line)
        line = fptr.readline()
    fptr.close()
    
    fptr = open('result_draw.txt')
    line = fptr.readline()
    line = fptr.readline()
    out.writelines("\n")
    while line:
        out.writelines(line)
        line = fptr.readline()
    fptr.close()
    
    fptr = open('part1.txt')
    line = fptr.readline()
    while line:
        out.writelines(line)
        line = fptr.readline()
    fptr.close()
    
    out.close()





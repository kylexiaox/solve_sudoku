__author__ = 'kyle_xiao'

import io

def readToArray(filename):
    file = open(filename)
    line = file.readline()
    listCsv = []
    while line!='':
        listCsv.append(line.split(','))
        line = file.readline()
    print(listCsv)
    return listCsv

def writeFromArray(filename,map):
    output = ''
    for col in range(len(map)):
        for row in range(len(map[col])):
            if row == 0:
                if map[col][row].number != None:
                    output = output + str(map[col][row].number)
                else:
                    output = output + str(map[col][row].cell)
            else:
                if map[col][row].number != None:
                    output = output +','+ str(map[col][row].number)
                else:
                    output = output +','+ str(map[col][row].cell)
        output = output+'\n'

    file = open(filename ,'w')
    file.write(output)




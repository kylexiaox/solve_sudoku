

__author__ = 'kyle_xiao'

import math
import csv


class Cell(object):
    _number = None
    _cell = None


    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        value = int(value)
        if (value > 9 or value < 1):
            raise ValueError('value must between 1 - 9!')
        self._number = value

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, value):
        self._cell = value

    def __init__(self, number):
        if number.strip().isdigit():
            self.number = number
        else:
            self.cell = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

class status(object):
    def __init__(self,map,row,col):
        self.map = map
        self.row = row
        self.col = col

class SolveSudoku(object):
    _map = [[Cell for col in range(9)] for row in range(9)]
    _setRow = [set() for row in range(9)]
    _setCol = [set() for col in range(9)]
    _setCell = [[set() for col in range(3)] for row in range(3)]
    _step_number = 0
    _isBottleneck = False
    _lastStableMap = None
    _statusStack = []

    def __init__(self, map):
        for row in range(9):
            for col in range(9):
                self._map[row][col] = Cell(map[row][col])
        self.flushSet()
        self._lastMap = self._map


    def flushSet(self):
        over = True
        for row in range(9):
            for col in range(9):
                if self._map[row][col].number != None:
                    self._setRow[row].add(self._map[row][col].number)
                    self._setCol[col].add(self._map[row][col].number)
                    self._setCell[int(math.ceil(row / 3))][int(math.ceil(col / 3))].add(self._map[row][col].number)
                else:
                    over = False
        self._step_number = self._step_number + 1
        print("flush Set, Setp: " + str(self._step_number) + "\n")
        self.printMap()
        csv.writeFromArray('middle_3.csv', self._map)
        return over


    def flushCell(self):
        for row in range(9):
            for col in range(9):
                if self._map[row][col].number == None:
                    # if len(self._map[row][col].cell) == 0:
                    #     recoverStatus = self._statusStack.pop()
                    #     self._map = recoverStatus.map
                    #     self._map[recoverStatus.row][recoverStatus.col].number = self._map[recoverStatus.row][recoverStatus.col].cell.pop()
                    #     self.flushSet()
                    #     return
                    self._map[row][col].cell = self._map[row][col].cell - self._setRow[row] - \
                                               self._setCell[int(math.ceil(row / 3))][int(math.ceil(col / 3))] - \
                                               self._setCol[col]
                    if len(self._map[row][col].cell) == 1:
                        self._map[row][col].number = self._map[row][col].cell.pop()
                    # elif self._isBottleneck == True and len(self._map[row][col].cell) == 2:
                    #     self._map[row][col].number = self._map[row][col].cell.pop()
                    #     currentStatus = status(self._map,row,col)
                    #     self._statusStack.append(currentStatus)
                    #     self._isBottleneck = False
                    else:
                        # row
                        temp = self._map[row][col].cell
                        for i in range(9):
                            if self._map[row][i].number == None and i != col:
                                temp = temp - self._map[row][i].cell
                        if len(temp) == 1:
                            self._map[row][col].number = temp.pop()
                            self._map[row][col].cell.clear()
                            continue
                        # col
                        temp = self._map[row][col].cell
                        for i in range(9):
                            if self._map[i][col].number == None and i != col:
                                temp = temp - self._map[i][col].cell
                        if len(temp) == 1:
                            self._map[row][col].number = temp.pop()
                            self._map[row][col].cell.clear()
                            continue
                        # cell
                        temp = self._map[row][col].cell
                        rowIndex = int(math.ceil(row / 3))
                        colIndex = int(math.ceil(col / 3))
                        for i in range(rowIndex, rowIndex + 3):
                            for j in range(colIndex, colIndex):
                                temp = temp - self._map[i][j].cell
                        if len(temp) == 1:
                            self._map[row][col].number = temp.pop()
                            self._map[row][col].cell.clear()
                            continue
        if not cmp(self._map, self._lastMap):
            self._isBottleneck = True

        self._lastMap = self._map

    def solveSudoku(self):
        while not self.flushSet():
            self.flushCell()
        result = []
        for row in range(9):
            subResult = []
            for col in range(9):
                subResult.append(self._map[row][col])
            result.append(subResult)
            csv.writeFromArray('result_3.csv', result)


    def printMap(self):
        output = ''
        for row in range(len(self._map)):
            for col in range(len(self._map[row])):
                if self._map[row][col].number != None:
                    output = output + ', ' + str(self._map[row][col].number)
                else:
                    output = output + ', 0'
            output = output + '\n'
        print(output)


if __name__ == '__main__':
    map = csv.readToArray('3.csv')
    SolveSudoku(map).solveSudoku();

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


class SolveSudoku(object):
    _map = [[Cell for col in range(9)] for row in range(9)]
    _setRow = [set() for row in range(9)]
    _setCol = [set() for col in range(9)]
    _setCell = [[set() for col in range(3)] for row in range(3)]
    _step_number = 0

    def __init__(self, map):
        for row in range(9):
            for col in range(9):
                self._map[row][col] = Cell(map[row][col])
        self.flushSet()


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
        return over


    def flushCell(self):
        for row in range(9):
            for col in range(9):
                if self._map[row][col].number == None:
                    self._map[row][col].cell = self._map[row][col].cell - self._setRow[row] - \
                                               self._setCell[int(math.ceil(row / 3))][int(math.ceil(col / 3))] - \
                                               self._setCol[col]
                    if len(self._map[row][col].cell) == 1:
                        self._map[row][col].number = self._map[row][col].cell.pop()

    def solveSudoku(self):
        while not self.flushSet():
            self.flushCell()
        result = []
        for row in range(9):
            subResult = []
            for col in range(9):
                subResult.append(self._map[row][col])
            result.append(subResult)
            csv.writeFromArray('result_1.csv', result)


    def printMap(self):
        output = ''
        for row in range(len(self._map)):
            for col in range(len(self._map[row])):
                output = output + ', ' + str(self._map[row][col].number)
            output = output + '\n'
        print(output)


if __name__ == '__main__':
    map = csv.readToArray('1.csv')
    SolveSudoku(map).solveSudoku();

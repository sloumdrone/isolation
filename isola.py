#!/usr/bin/env python
# -*- coding: utf-8 -*-
from isola_ai import Opponent

class Isola:
    def __init__(self):
        self.game_board = [ [ ' - ' for y in range(7) ] for x in range(7) ]
        self.turn = 0
        self.move_counter = 0
        self.pieces = [' X ',' O ']
        self.coords = [[0,3],[6,3]]
        self.opponent = Opponent(self)

        self.game_board[self.coords[0][0]][self.coords[0][1]] = self.pieces[0]
        self.game_board[self.coords[1][0]][self.coords[1][1]] = self.pieces[1]

        self.loop()

    def print_board(self):
        print '\n\n'
        print '    ' + ''.join([' ' + str(i) + ' ' for i in range(7)])
        for x in range(7):
            print '   ' + str(x) + ''.join(self.game_board[x])
        print "\n     Player {0}'s turn:\n".format(self.pieces[self.turn].strip())

    def loop(self):
        while 1:
            self.print_board()

            if self.turn == 0:
                if not self.check_game_over(self.coords[0][0],self.coords[0][1]):
                    print '\nPlayer O wins!\n\n'
                    break

                try:
                    print ' Move to an adjacent tile'
                    moveRow = int(raw_input(' Row? '))
                    moveCol = int(raw_input(' Col? '))
                    move = [moveRow,moveCol]
                except ValueError:
                    print '\nInvalid move entry. Please try again.'
                    continue

                try:
                    print ' Destroy ANY unoccupied tile'
                    destroyRow = int(raw_input(' Row? '))
                    destroyCol = int(raw_input(' Col? '))
                    destroy = [destroyRow,destroyCol]
                except ValueError:
                    print '\nInvalid destruction entry. Please try again.'
                    continue


                if not self.validate_moves(destroy,move):
                    print '\nIllegal play. Try again.'
                    continue
            else:
                # ai moves
                old_position = self.coords[1]
                move_list = self.opponent.take_turn()

                if move_list:
                    self.game_board[move_list['move'][0]][move_list['move'][1]] = self.pieces[self.turn]
                    self.game_board[move_list['destruction'][0]][move_list['destruction'][1]] = '   '
                    if self.move_counter < 2:
                        self.game_board[old_position[0]][old_position[1]] = '   '
                    else:
                        self.game_board[old_position[0]][old_position[1]] = ' - '
                    self.coords[1] = [move_list['move'][0],move_list['move'][1]]
                    print ' Move: {}-{}'.format(move_list['move'][0],move_list['move'][1])
                    print ' Destruction: {}-{}'.format(move_list['destruction'][0],move_list['destruction'][1])
                else:
                    print '\nPlayer X wins!\n\n'
                    break


            self.turn = abs(self.turn - 1)
            self.move_counter += 1



    def validate_moves(self,dest,mov):
        old_position = self.coords[self.turn]
        if dest[0] < 0 or dest[0] > 6 or dest[1] < 0 or dest[1] > 6 or self.game_board[dest[0]][dest[1]] != ' - ':
            return False

        if mov[0] < 0 or mov[0] > 6 or mov[1] < 0 or mov[1] > 6 or self.game_board[mov[0]][mov[1]] != ' - ':
            return False

        if abs(mov[0] - self.coords[self.turn][0]) > 1 or abs(mov[1] - self.coords[self.turn][1]) > 1:
            return False

        if mov[0] == dest[0] and mov[1] == dest[1]:
            return False

        self.game_board[mov[0]][mov[1]] = self.pieces[self.turn]
        self.game_board[dest[0]][dest[1]] = '   '
        if self.move_counter < 2:
            self.game_board[old_position[0]][old_position[1]] = '   '
        else:
            self.game_board[old_position[0]][old_position[1]] = ' - '
        self.coords[self.turn] = [mov[0],mov[1]]
        return True

    def check_game_over(self,row,col):
        board = self.game_board
        if (row + 1 <= 6 and board[row + 1][col] == ' - ') or (col + 1 <= 6 and board[row][col + 1] == ' - ') or (row - 1 >= 0 and board[row - 1][col] == ' - ') or (col - 1 >= 0 and board[row][col - 1] == ' - ') or (row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] == ' - ') or (row + 1 <= 6 and col + 1 <= 6 and board[row + 1][col + 1] == ' - ') or (row + 1 <= 6 and col - 1 >= 0 and board[row + 1][col - 1] == ' - ') or (row - 1 >= 0 and col + 1 <= 6 and board[row - 1][col + 1] == ' - '):
            return True
        return False



if __name__ == "__main__":
    print '''
  _____                 _
 |_   _|               | |
   | |    ___    ___   | |   __ _
   | |   / __|  / _ \  | |  / _` |
  _| |_  \__ \ | (_) | | | | (_| |
 |_____| |___/  \___/  |_|  \__,_|
                                  '''
    gmae = Isola()

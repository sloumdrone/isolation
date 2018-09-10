#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

class Opponent:
    def __init__(self,parent):
        self.game = parent
        self.legal_moves = []

    def get_legal_moves(self,row,col,arr):
        board = self.game.game_board
        if row + 1 <= 6 and board[row + 1][col] == ' - ':
            arr.append({'row': row + 1, 'col': col, 'points': 0})
        if col + 1 <= 6 and board[row][col + 1] == ' - ':
            arr.append({'row': row, 'col': col + 1, 'points': 0})
        if row - 1 >= 0 and board[row - 1][col] == ' - ':
            arr.append({'row': row - 1, 'col': col, 'points': 0})
        if col - 1 >= 0 and board[row][col - 1] == ' - ':
            arr.append({'row': row, 'col': col - 1, 'points': 0})
        if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] == ' - ':
            arr.append({'row': row - 1, 'col': col - 1, 'points': 0})
        if row + 1 <= 6 and col + 1 <= 6 and board[row + 1][col + 1] == ' - ':
            arr.append({'row': row + 1, 'col': col + 1, 'points': 0})
        if row + 1 <= 6 and col - 1 >= 0 and board[row + 1][col - 1] == ' - ':
            arr.append({'row': row + 1, 'col': col - 1, 'points': 0})
        if row - 1 >= 0 and col + 1 <= 6 and board[row - 1][col + 1] == ' - ':
            arr.append({'row': row - 1, 'col': col + 1, 'points': 0})


    def choose_best_move(self):
        point_distribution = []

        for move in self.legal_moves:
            self.get_legal_moves(move['row'],move['col'],point_distribution)
            move['points'] = len(point_distribution)
            point_distribution = []
        best_score = self.get_max_points(self.legal_moves)

        return [[x['row'],x['col']] for x in self.legal_moves if x['points'] == best_score]


    def choose_best_destruction(self):
        point_distribution = []
        cpu_compare_moves = []
        p1_legals = []

        # Set legal moves to player 1's legal moves
        self.get_legal_moves(self.game.coords[0][0],self.game.coords[0][1],p1_legals)

        if len(p1_legals):
            for destruction in p1_legals:
              self.get_legal_moves(destruction['row'],destruction['col'],point_distribution)
              destruction['points'] = len(point_distribution)
              point_distribution = []
            self.get_legal_moves(self.game.coords[1][0],self.game.coords[1][1],cpu_compare_moves)
            for p2 in cpu_compare_moves:
                for p1 in p1_legals:
                    if p2['row'] == p1['row'] and p2['col'] == p1['col']:
                        p1['points'] = max(0,p1['points'] - 2)
            best_score = self.get_max_points(p1_legals)
            return [[x['row'],x['col']] for x in p1_legals if x['points'] == best_score]
        else:
            # Choose a random destruction point if enemy is surrounded
            # prevents hang on death hit
            for r in range(10):
                for c in range(10):
                    if self.game.game_board[r][c] == ' - ':
                        return [[r,c]]

    def get_max_points(self,arr):
        return max([x['points'] for x in arr])

    def take_turn(self):
        self.legal_moves = []

        # Get move options and choose the best move
        self.get_legal_moves(self.game.coords[1][0],self.game.coords[1][1],self.legal_moves)
        if not len(self.legal_moves):
            return False
        best_move = random.choice(self.choose_best_move())

        # Get destruction options and choose the best destruction
        best_destruction = random.choice(self.choose_best_destruction())

        return {'move': best_move, 'destruction': best_destruction}

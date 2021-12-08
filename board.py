class Board:
    turns = ['X', 'Y']
    game_end = False

    def __init__(self) -> None:
        self.board = [
            '', '', '',
            '', '', '',
            '', '', ''
        ]
        self.turn = 0
        self.bottom_text = "Turn : "+str(self.turns[self.turn])

    def set_board_box(self, sym, pos):
        self.board[pos] = sym

    def win_check(self):
        b = self.board
        for sym in self.turns:
            if (
                (b[0] == sym and b[1] == sym and b[2] == sym) or
                (b[3] == sym and b[4] == sym and b[5] == sym) or
                (b[6] == sym and b[7] == sym and b[8] == sym) or

                (b[0] == sym and b[3] == sym and b[6] == sym) or
                (b[1] == sym and b[4] == sym and b[7] == sym) or
                (b[2] == sym and b[5] == sym and b[8] == sym) or

                (b[0] == sym and b[4] == sym and b[8] == sym) or
                (b[2] == sym and b[4] == sym and b[6] == sym)
                ):
                self.game_end = True
                return sym
        return False
    
    def click_check(self, sym_val, sym_pos):
        btn_sym = sym_val

        if (not self.game_end):
            if (btn_sym not in self.turns):
                sym = self.turns[self.turn]
                btn_sym = sym
                
                self.turn = 0 if self.turn == 1 else 1
                self.set_board_box(sym, sym_pos)

                chk = self.win_check()
                if (chk):
                    self.bottom_text = chk+" has won"
                    self.game_end = True
                else:
                    self.bottom_text = 'Turn: '+str(self.turns[self.turn])
                    if '' not in self.board:
                        self.bottom_text = 'Tie'
                        self.game_end = True
        else:
            self.board = [
                '', '', '',
                '', '', '',
                '', '', ''
            ]
            btn_sym = ''
            self.game_end = False
            
        return btn_sym
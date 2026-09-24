from UI import UI
from Logic import Logic

print("Chess Game Running")
UI.REDRAW()
UI.CHESS_BOARD.bind("<Button-1>", Logic.ON_CLICK)
UI.CHESS_BOARD.pack()
UI.GAME_FRAME.mainloop()
import coreli.tinytiles as tt


Collatz_tileset: tt.Tileset = [(0,0,0,0),(0,1,1,0),(0,2,0,1),
                   (1,0,1,1),(1,1,0,2),(1,2,1,2)]
    
Extended_Collatz_tileset: tt.Tileset = [(0,0,0,0),(0,1,1,0),(0,2,0,1),
                   (1,0,1,1),(1,1,0,2),(1,2,1,2),(1,'S',0,2),(0,'S',0,'S')]
import drawSvg as draw
from coreli.tinytiles.model import Tileset, Tiling

TILE_SIZE = 32
null_glue_color = "#CACACA"
color_wheel = {0:"#E6C58F",1:"#0AC52E",2:"#E37998",'S':'#3FB3F3'}

def draw_tile(d,x,y,tile,tileset:Tileset=[],debug=False):
    draw_x, draw_y = TILE_SIZE*x, TILE_SIZE*y
    
    tile_group = draw.Group()
    
    if debug:
        r = draw.Rectangle(draw_x,draw_y,TILE_SIZE,TILE_SIZE,fill="red")
        tile_group.children.append(r)
        
    
    tile_center_x = draw_x+TILE_SIZE/2
    tile_center_y = draw_y+TILE_SIZE/2
    
    a = [-1,1,1,-1]
    b = [1,1,-1,-1]
    c = [1,0,-1,0]
    e = [0,-1,0,1]
    
    r = draw.Rectangle(draw_x,draw_y,TILE_SIZE,TILE_SIZE,fill=None,stroke="gray",stroke_width=1)
    tile_group.children.append(r)
    
    
    
    
    
    # glue colors
    for side in range(0,4):
        glue = tile[side]
        color = null_glue_color
        if glue is not None:
            color = color_wheel[glue]
        p = draw.Path(stroke_width=1, stroke=None,
              fill=color, fill_opacity=1, marker_end=None)
        p.M(tile_center_x, tile_center_y)
        p.l(a[side]*(TILE_SIZE/2),b[side]*(TILE_SIZE/2)) 
        p.l(c[side]*(TILE_SIZE),e[side]*(TILE_SIZE))
        p.Z()
        tile_group.children.append(p)
        
    p = draw.Path(stroke_width=0.4, stroke="gray",
              fill=None, fill_opacity=0, marker_end=None)
    p.M(draw_x, draw_y)
    p.l(TILE_SIZE,TILE_SIZE) 
    tile_group.children.append(p)
    
    p = draw.Path(stroke_width=0.4, stroke="gray",
              fill=None, fill_opacity=0, marker_end=None)
    p.M(draw_x+TILE_SIZE, draw_y)
    p.l(-1*TILE_SIZE,TILE_SIZE) 
    tile_group.children.append(p)
    
    # glue names
    for side in range(0,4):
        glue = tile[side]
        if glue is not None:
            tile_group.children.append(draw.Text(str(glue), 8, 
                           tile_center_x+(a[side]+c[side])*(TILE_SIZE/2)+3.7*e[side], 
                           tile_center_y+(b[side]+e[side])*(TILE_SIZE)/2-4.2*c[side], 
                           fill='black',text_anchor="middle",valign='middle', font_family="Arimo"))
    
    # tile name (if any)
    if tile in tileset:
        tweak_offset_y = 0.5
        # HACK UGLY
        tile_name = str(tileset.index(tile))
        if tile_name == '6':
            tile_name = 'R'
        if tile_name == '7':
            tile_name = 'S'
        tile_group.children.append(draw.Text(str(tile_name), 16, 
                           tile_center_x, tile_center_y+tweak_offset_y, fill='black',
                           text_anchor="middle",valign='middle',font_weight="bold",font_family="Arimo")) 
        

        
    d.append(tile_group)

def draw_tiling(tiling: Tiling, debug=False, filter_pos=lambda x,y: True):
    world_w, world_h = tiling.get_world_boundaries()
    
    draw_w, draw_h = TILE_SIZE*(world_w+1), TILE_SIZE*(world_h+1)
    
    d = draw.Drawing(draw_w, draw_h, origin=(0,0), displayInline=False)
    if debug:
        r = draw.Rectangle(0,0,draw_w,draw_h,fill="blue")
        d.append(r)
    for x,y in tiling.tiling.keys():
        if filter_pos(x,y):
            draw_tile(d,x,y,tiling[x,y],tiling.tileset,debug)
    if debug:
        r = draw.Rectangle(0,0,TILE_SIZE,TILE_SIZE,fill="lime",fill_opacity=0.6)
        d.append(r)
    return d
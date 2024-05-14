from tiles.typeTiles.simpleTile import Tile
from tiles.typeTiles.simpleTile import SimpleTile
from tiles.typeTiles.doubleTile import DoubleTile

if __name__ == "__main__":
    myTile = SimpleTile(1, 2)
    myTile.printTile()
    myTile2 = myTile.clone()
    myTile2.printTile()
    print(myTile2.getSide1)
    myTile2.setSide1 = 4
    myTile2.printTile()
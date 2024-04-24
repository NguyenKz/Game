def collision(object_1,object_2)->bool:
    rect1 = [object_1.x,object_1.y,object_1.x+object_1.w,object_1.y+object_1.h]
    rect2 = [object_2.x,object_2.y,object_2.x+object_2.w,object_2.y+object_2.h]
    if rect1[0] > rect2[2] or rect2[0] > rect1[2]:
        return False

    if rect1[1] > rect2[3] or rect2[1] > rect1[3]:
        return False

    return True

class Ob:

    def __init__(self,x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h


ob1 = Ob(670,131,40,40)
ob2 = Ob(702,156,30,30)

print(collision(ob1,ob2))
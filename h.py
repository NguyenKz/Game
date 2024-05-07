def point_in_rectangle(point, rectangle):
    x, y = point
    x1, y1, x2, y2 = rectangle
    
    # Kiểm tra xem điểm có nằm trong hình chữ nhật không
    if (min(x1, x2) <= x <= max(x1, x2) and
        min(y1, y2) <= y <= max(y1, y2)):
        return True
    else:
        return False

# Ví dụ về hình chữ nhật được xác định bởi hai đỉnh (x1, y1) và (x2, y2)
rectangle = (1, 1, 4, 3)
# Điểm cần kiểm tra
point = (2, 10)

if point_in_rectangle(point, rectangle):
    print("Điểm nằm trong hình chữ nhật.")
else:
    print("Điểm không nằm trong hình chữ nhật.")

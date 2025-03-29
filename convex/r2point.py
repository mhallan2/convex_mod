from math import sqrt, inf, acos, degrees


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Нахождение угла как между векторами, так и отрезками/прямыми
    @staticmethod
    def angle_dot_product(a, b, c, d, text='as vectors'):
        angle = 0.0
        dx1, dy1 = a.x - b.x, a.y - b.y
        dx2, dy2 = c.x - d.x, c.y - d.y
        len1 = R2Point.dist(a, b)
        len2 = R2Point.dist(c, d)
        if len1 == 0 or len2 == 0:
            return 0.0
        if text == 'as vectors':
            angle = acos((dx1 * dx2 + dy1 * dy2) /
                         (R2Point.dist(a, b) * R2Point.dist(c, d)))
        elif text == 'as straight lines':
            angle = acos(
                abs((dx1 * dx2 + dy1 * dy2) /
                    (R2Point.dist(a, b) * R2Point.dist(c, d))))
        return degrees(angle)

    # Определяем под каким углом пересекаются именно отрезки
    @staticmethod
    def angle_segments(a, b, c, d):
        angle = 0.0
        intersect = R2Point.line_intersection(a, b, c, d)
        if intersect and intersect is not inf:
            if b == c:
                angle = R2Point.angle_dot_product(b, a, c, d)
            elif b == d:
                angle = R2Point.angle_dot_product(b, a, d, c)
            elif a == c:
                angle = R2Point.angle_dot_product(a, b, c, d)
            elif a == d:
                angle = R2Point.angle_dot_product(a, b, d, c)
            else:
                angle = R2Point.angle_dot_product(a, b, c, d,
                                                  'as straight lines')
        angle = round(angle, 2)
        return angle

    @staticmethod
    def task_angle(*points):
        angle = R2Point.angle_segments(*points)
        return angle if angle <= 45.0 else 0.0

    @staticmethod
    def line_intersection(a, b, c, d):

        dx1, dy1 = b.x - a.x, b.y - a.y
        dx2, dy2 = d.x - c.x, d.y - c.y
        dx3, dy3 = a.x - c.x, a.y - c.y

        # Определители
        det = dx1 * dy2 - dx2 * dy1  # Линейная зависимость векторов
        det1 = dx1 * dy3 - dx3 * dy1
        det2 = dx2 * dy3 - dx3 * dy2

        if det == 0.0:  # Отрезки параллельны
            if det1 != 0.0 or det2 != 0.0:  # Не лежат на одной прямой
                return None

            overlap_x = (min(a.x, b.x) < max(c.x, d.x)) and (min(c.x, d.x)
                                                             < max(a.x, b.x))
            overlap_y = (min(a.y, b.y) < max(c.y, d.y)) and (min(c.y, d.y)
                                                             < max(a.y, b.y))

            if overlap_x or overlap_y:
                return inf

            else:
                if a == c or a == d:
                    return a
                elif b == c or b == d:
                    return b

        s = det1 / det
        t = det2 / det
        inter_point = R2Point(a.x + t * dx1, a.y + t * dy1)
        if 0.0 <= s <= 1.0 and 0.0 <= t <= 1.0:
            return inter_point

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x))
                and ((a.y <= self.y and self.y <= b.y) or
                     (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

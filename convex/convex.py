from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def angle(self):
        return 0.0

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)


class Polygon(Figure):
    """ "Многоугольник" """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._task_angle = 0.0

        edge_first = (a, b)
        edge_second = (c, a)
        edge_third = (b, c)
        self._task_angle += (
            R2Point.task_angle(*edge_first, *edge_second) +
            R2Point.task_angle(*edge_second, *edge_third) +
            R2Point.task_angle(*edge_third, *edge_first))

    def angle(self):
        return self._task_angle

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(
                R2Point.area(t, self.points.last(), self.points.first()))

            # запоминаем текущее ребро для случаев,
            # когда обходим оболочку в разных направлениях
            curr_first_point = self.points.first()
            curr_last_point = self.points.last()

            lighted_edge_clock = (curr_first_point, curr_last_point)
            lighted_edge_counterclock = (curr_first_point, curr_last_point)

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))

                gotten_first = p
                rotated_first = self.points.first()
                curr_edge_counterclock = (gotten_first, rotated_first)
                self._task_angle -= R2Point.task_angle(
                    *lighted_edge_counterclock, *curr_edge_counterclock)
                lighted_edge_counterclock = (gotten_first, rotated_first)
                p = self.points.pop_first()
            else:
                gotten_first = p
                rotated_first = self.points.first()
                adding_point = t

                unlighted_edge_counterclock = (rotated_first, gotten_first)
                adding_edge = (adding_point, gotten_first)
                curr_edge_counterclock = (gotten_first, rotated_first)

                self._task_angle -= R2Point.task_angle(
                    *lighted_edge_counterclock, *curr_edge_counterclock)
                self._task_angle += R2Point.task_angle(
                    *adding_edge, *unlighted_edge_counterclock)
            self.points.push_first(p)
            curr_first_point = self.points.first()

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))

                gotten_last = p
                rotated_last = self.points.last()
                curr_edge_clock = (gotten_last, rotated_last)
                self._task_angle -= R2Point.task_angle(
                    *lighted_edge_clock, *curr_edge_clock)
                lighted_edge_clock = (gotten_last, rotated_last)
                p = self.points.pop_last()
            else:
                gotten_last = p
                rotated_last = self.points.last()
                adding_point = t

                unlighted_edge_clock = (rotated_last, gotten_last)
                adding_edge = (adding_point, gotten_last)
                curr_edge_clock = (gotten_last, rotated_last)

                self._task_angle -= R2Point.task_angle(
                    *lighted_edge_clock, *curr_edge_clock)
                self._task_angle += R2Point.task_angle(
                    *adding_edge, *unlighted_edge_clock)
            self.points.push_last(p)
            curr_last_point = self.points.last()

            # добавление двух новых рёбер
            new_edge_first = (adding_point, curr_first_point)
            new_edge_second = (adding_point, curr_last_point)

            self._task_angle += R2Point.task_angle(
                *new_edge_first, *new_edge_second)
            self._perimeter += (t.dist(self.points.first()) +
                                t.dist(self.points.last()))
            self.points.push_first(t)

        return self

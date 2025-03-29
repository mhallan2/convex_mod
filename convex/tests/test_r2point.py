from pytest import approx
from math import sqrt, inf
from r2point import R2Point
from mock import mock


class TestR2Point:

    # Точку можно создать через стандартный поток ввода
    def test_r2point_input(self):
        coords = iter(["1", "2"])
        with mock.patch('builtins.input', lambda _: next(coords)):
            assert R2Point() == R2Point(1.0, 2.0)

    # Угол между нуль-вектором и ненулевым определим как 0
    def test_angle_dot_product0(self):
        a = R2Point(0.0, 0.0)
        b = R2Point(0.0, 0.0)
        c = R2Point(0.0, 0.0)
        d = R2Point(1.0, 0.0)
        angle = R2Point.angle_dot_product(a, b, c, d)
        assert angle == approx(0.0)

    # Острый угол между векторами ab и cd
    def test_angle_dot_product1(self):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 1.0)
        c = R2Point(0.0, 0.0)
        d = R2Point(1.0, 0.0)
        angle = R2Point.angle_dot_product(a, b, c, d)
        assert angle == approx(45.0)

    # Тупой угол между векторами ab и cd
    def test_angle_dot_product2(self):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 1.0)
        c = R2Point(0.0, 0.0)
        d = R2Point(-1.0, 0.0)
        angle = R2Point.angle_dot_product(a, b, c, d)
        assert angle == approx(135.0)

    # Угол между "прямыми" ab и cd
    def test_angle_dot_product3(self):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 1.0)
        c = R2Point(0.0, 0.0)
        d = R2Point(-1.0, 0.0)
        angle = R2Point.angle_dot_product(a, b, c, d, 'as straight lines')
        assert angle == approx(45.0)

    # Угол между векторами ab и cd не с общим началом
    def test_angle_dot_product4(self):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 1.0)
        c = R2Point(-2.0, 0.0)
        d = R2Point(-3.0, 0.0)
        angle = R2Point.angle_dot_product(a, b, c, d)
        assert angle == approx(135.0)

    # Угол между сонаправленными векторами ab и cd
    def test_angle_dot_product5(self):
        a = R2Point(0.0, 0.0)
        b = R2Point(1.0, 1.0)
        c = R2Point(2.0, 2.0)
        d = R2Point(3.0, 3.0)
        angle = R2Point.angle_dot_product(a, b, c, d)
        assert angle == approx(0.0, abs=1e-5)

    # Угол между противонаправленными векторами ab и cd
    def test_angle_dot_product6(self):
        a = R2Point(1.0, 1.0)
        b = R2Point(0.0, 0.0)
        c = R2Point(2.0, 2.0)
        d = R2Point(3.0, 3.0)
        angle = R2Point.angle_dot_product(a, b, c, d)
        assert angle == approx(180.0)

    # Угол между совпадающими отрезками
    def test_task_angle_lines1(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(0, 0), R2Point(1, 1))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(0.0, abs=1e-5)

    # Угол между отрезками внахлест
    def test_task_angle_lines2(self):
        line1 = (R2Point(0, 0), R2Point(2, 2))
        line2 = (R2Point(1, 1), R2Point(3, 3))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(0.0, abs=1e-5)

    # Угол между отрезками с совпавшей вершиной
    def test_task_angle_lines3(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(-1, 0), R2Point(0, 0))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(0.0)

    # Угол между отрезками с одной из вершин на другом отрезке
    def test_task_angle_lines4(self):
        line1 = (R2Point(0, 0), R2Point(2, 0))
        line2 = (R2Point(1, 0), R2Point(2, 1))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(45.0)

    # Угол между пересекающимися отрезками
    def test_task_angle_lines5(self):
        line1 = (R2Point(-1, -1), R2Point(1, 1))
        line2 = (R2Point(-1, 0), R2Point(1, 0))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(45.0)

    # Угол больше 45 градусов между пересекающимися отрезками
    def test_task_angle_lines6(self):
        line1 = (R2Point(0, 0), R2Point(2, 2))
        line2 = (R2Point(0, 1), R2Point(1, 0))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(0.0)

    # Угол между непересекающимися отрезками будем считать нейтральным
    def test_task_angle_lines7(self):
        line1 = (R2Point(1, 1), R2Point(2, 2))
        line2 = (R2Point(0, 0), R2Point(1, 0))
        angle = R2Point.task_angle(*line1, *line2)
        assert angle == approx(0.0)

    # Совпадающие отрезки
    def test_line_intersection1(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(0, 0), R2Point(1, 1))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect is inf

    # Отрезок внутри другого, одна общая вершина
    def test_line_intersection2(self):
        line1 = (R2Point(0, 0), R2Point(2, 2))
        line2 = (R2Point(0, 0), R2Point(1, 1))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect is inf

    # Отрезок внутри другого, без общих вершин
    def test_line_intersection3(self):
        line1 = (R2Point(0, 0), R2Point(3, 3))
        line2 = (R2Point(1, 1), R2Point(2, 2))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect is inf

    # Отрезки на одной прямой, касаются в общей вершине
    #   неважно в какой последовательности указаны точки
    def test_line_intersection4(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(1, 1), R2Point(2, 2))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect == R2Point(1, 1)

    #   наоборот
    def test_line_intersection5(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(2, 2), R2Point(1, 1))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect == R2Point(1, 1)

    #   еще наоборот
    def test_line_intersection6(self):
        line1 = (R2Point(1, 1), R2Point(0, 0))
        line2 = (R2Point(2, 2), R2Point(1, 1))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect == R2Point(1, 1)

    # Отрезки не на одной прямой, касаются в общей вершине
    def test_line_intersection7(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(1, 1), R2Point(2, 3))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect == R2Point(1, 1)

    # Отрезки параллельны
    def test_line_intersection8(self):
        line1 = (R2Point(0, 0), R2Point(0, 1))
        line2 = (R2Point(2, 0), R2Point(2, 1))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect is None

    # Отрезки не пересекаются, не параллельны
    def test_line_intersection9(self):
        line1 = (R2Point(0, 0), R2Point(1, 1))
        line2 = (R2Point(0, 1), R2Point(3, 2))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect is None

    # Стандартное пересечение отрезков
    def test_line_intersection10(self):
        line1 = (R2Point(0, 0), R2Point(2, 2))
        line2 = (R2Point(0, 1.5), R2Point(3, 0))
        intersect = R2Point.line_intersection(*line1, *line2)
        assert intersect == R2Point(1, 1)

    # Расстояние от точки до самой себя равно нулю
    def test_dist1(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 1.0)) == approx(0.0)

    # Расстояние между двумя различными точками положительно
    def test_dist2(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(1.0, 0.0)) == approx(1.0)

    def test_dist3(self):
        a = R2Point(1.0, 1.0)
        assert a.dist(R2Point(0.0, 0.0)) == approx(sqrt(2.0))

    # Площадь треугольника равна нулю, если все вершины совпадают
    def test_area1(self):
        a = R2Point(1.0, 1.0)
        assert R2Point.area(a, a, a) == approx(0.0)

    # Площадь треугольника равна нулю, если все вершины лежат на одной прямой
    def test_area2(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 1.0), R2Point(2.0, 2.0)
        assert R2Point.area(a, b, c) == approx(0.0)

    # Площадь треугольника положительна при обходе вершин против часовой
    # стрелки
    def test_area3(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, b, c) > 0.0

    # Площадь треугольника отрицательна при обходе вершин по часовой стрелке
    def test_area4(self):
        a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
        assert R2Point.area(a, c, b) < 0.0

    # Точки могут лежать внутри и вне "стандартного" прямоугольника с
    # противоположными вершинами (0,0) и (2,1)
    def test_is_inside1(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(a, b)

    def test_is_inside2(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert R2Point(1.0, 0.5).is_inside(b, a)

    def test_is_inside3(self):
        a, b = R2Point(0.0, 0.0), R2Point(2.0, 1.0)
        assert not R2Point(1.0, 1.5).is_inside(a, b)

    # Ребро [(0,0), (1,0)] может быть освещено или нет из определённой точки
    def test_is_light1(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert not R2Point(0.5, 0.0).is_light(a, b)

    def test_is_light2(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(2.0, 0.0).is_light(a, b)

    def test_is_light3(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert not R2Point(0.5, 0.5).is_light(a, b)

    def test_is_light4(self):
        a, b = R2Point(0.0, 0.0), R2Point(1.0, 0.0)
        assert R2Point(0.5, -0.5).is_light(a, b)

    # Две точки различны
    def test_eq1(self):
        assert R2Point(1.0, 1.0) != R2Point(2.0, 2.0)

    # Точка и кортеж отличаются
    def test_eq2(self):
        assert R2Point(1.0, 1.0) != (1.0, 1.0)

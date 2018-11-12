"""
Some helper methods.
Maybe split it to other modules?
"""

import inspect


def get_csrf_token_from_request(request):
    """
    Take csrf token from given request

    :param request: request to server
    :return: csrf token
    :rtype: str
    """
    return request.META.get('CSRF_COOKIE', None)


def coordinates_to_abs(relative_coordinates, pic_size_x, pic_size_y):
    """
    Convert relative coordinates (cell coordinates) to absolute coordinates
    (x, y of top left corner of image)
    using to know image place on html page

    :param relative_coordinates: relative coordinates of cell
    :param pic_size_x: picture x size
    :param pic_size_y: picture y size
    :return: image top left corner x, y coordinates
    :type relative_coordinates: list
    :type pic_size_x: int
    :type pic_size_y: int
    :rtype: tuple
    """

    cell_size = 42
    cell_indent_x = 96
    cell_indent_y = 200
    cos_30 = 3**0.5 / 2
    sin_30 = 0.5

    if relative_coordinates[1] % 2 == 0:
        add_x = 0 + cell_size * cos_30
    else:
        add_x = 0

    x = int(
        cell_indent_x + 2 * (
            cell_size*cos_30
        ) * relative_coordinates[0] - (pic_size_x / 2) + add_x)
    y = int(
        cell_indent_y + (
            cell_size + cell_size*sin_30
        ) * relative_coordinates[1] - (pic_size_y - 20)
    )

    return x, y


def coordinates_to_relative(absolute_coordinates):
    """
    Convert absolute coordinates to relative coordinates (cell coordinates)
    and vector relative to center of cell
    using to calculate which cell user click on battle field
    and on which direction

    :param absolute_coordinates: absolute coordinates
    :return: cell coordinates and vector
    :type absolute_coordinates: list
    :rtype: tuple
    """
    cell_size = 42
    circle_rad = int(cell_size * 3**0.5 / 2)
    for x_cell in range(0, 15):
        for y_cell in range(0, 11):
            tmp_coordinates = coordinates_to_abs([x_cell, y_cell], 0, 20)
            dx = tmp_coordinates[0] - absolute_coordinates[0]
            dy = tmp_coordinates[1] - absolute_coordinates[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist <= circle_rad:
                if dist != 0:
                    x_vector = dx / dist
                    y_vector = dy / dist
                else:
                    x_vector = 0
                    y_vector = 0

                return (x_cell, y_cell), (x_vector, - y_vector)

    return None


def cells_distance(point_a, point_b):
    """
    Method to calculate distance between two cells on field
    take coordinates of two cells, returns shorter distance between this cells

    :param point_a: coordinates of first cell
    :param point_b: coordinates of second cell
    :return: distance between two cells
    :type point_a: tuple
    :type point_b: tuple
    :rtype: int
    """
    delta_y = int(abs(point_a[1] - point_b[1]))
    koeff = delta_y / 2
    koeff_a = 0
    koeff_b = 0

    if delta_y % 2 == 1:
        koeff_b = 0.5

        if point_a[1] % 2 == 1:
            koeff_a = -0.5
        else:
            koeff_a = 0.5

        if (point_a[0] + koeff_a) < point_b[0]:
            koeff_b = -0.5

    distance = round(
        abs((point_a[0] + koeff_a) - (point_b[0] + koeff_b)) + koeff, 1)

    return distance


def get_attacker_cell(coordinates, vectors):
    """
    Calculate cell to move attacker to it
    using to check if it possible to attack some unit,
    and if possible, so to which cell move attacker then

    :param coordinates: click coordinates probably coordinates of defender unit
    :param vectors: click vector (it have matter)
    :return: new attacker cells coordinates
    :type coordinates: tuple
    :type vectors: tuple
    :rtype: tuple
    """
    if vectors[0] > 0:
        if abs(vectors[1]) < 0.5:
            x_cell = coordinates[0] - 1
            y_cell = coordinates[1]
        else:
            x_cell = coordinates[0]
            if coordinates[1] % 2 == 1:
                x_cell -= 1
            y_cell = coordinates[1] + int(vectors[1] / abs(vectors[1]))
    else:
        if abs(vectors[1]) < 0.5:
            x_cell = coordinates[0] + 1
            y_cell = coordinates[1]
        else:
            x_cell = coordinates[0]
            if coordinates[1] % 2 == 0:
                x_cell += 1
            y_cell = coordinates[1] + int(vectors[1] / abs(vectors[1]))

    return int(x_cell), int(y_cell)


def range_damage(attacker_coordinates, target_coordinates):
    """
    Method to calculate ranged damage coefficient,
    based on distance between units
    returns 0.5 if distance more than 9 hexes
    returns 0 if units stay close (adjacent cells)
    returns 1 if distance between units more than 1 and less than 10

    :param attacker_coordinates: coordinates of attacker unit
    :param target_coordinates: coordinates of target unit
    :return: range damage coefficient (0 or 0.5 or 1)
    :type attacker_coordinates: tuple
    :type target_coordinates: tuple
    :rtype: float
    """
    distance = cells_distance(attacker_coordinates, target_coordinates)

    if distance == 1:
        range_damage_coefficient = 0
    elif distance >= 10:
        range_damage_coefficient = 0.5
    else:
        range_damage_coefficient = 1

    return range_damage_coefficient


def dragon_breath_coordinates(attacker_coordinates, target_coordinates):
    """
    Method to calculate second target coordinates for dragon breath attack
    based on attacker unit (with dragon breath) and defender unit coordinates

    :param attacker_coordinates:
        attacker unit (unit with dragon breath attack) coordinates
    :param target_coordinates:
        target unit (unit who take first attack) coordinates
    :return:second target coordinates which should be checked,
        maybe no unit there
    :type attacker_coordinates: tuple
    :type target_coordinates: tuple
    :rtype: tuple
    """
    if (target_coordinates[1] - attacker_coordinates[1]) == 0:
        x = 2 * target_coordinates[0] - attacker_coordinates[0]
        y = target_coordinates[1]
    else:
        y = 2 * target_coordinates[1] - attacker_coordinates[1]
        if target_coordinates[1] % 2 == 1:
            x = 2 * target_coordinates[0] - attacker_coordinates[0] - 1
        else:
            x = 2 * target_coordinates[0] - attacker_coordinates[0] + 1

    return x, y


def get_special_methods(module_to_search, names_to_search):
    """
    Get all methods (most probably specials methods) from module by names
    using to get unit specials or effects methods by names

    :param module_to_search: module to search methods in
    :param names_to_search: names of methods to search in module
    :return: founded methods in module with needed names only
    :type module_to_search: module
    :type names_to_search: iterable
    :rtype: list
    """
    module_methods = inspect.getmembers(module_to_search, inspect.isfunction)

    methods_to_return = list()
    for name, method in module_methods:
        if name in names_to_search:
            methods_to_return.append(method)

    return methods_to_return


def get_nearby_cells(cell_coordinates):
    """
    Get all cells which are adjacent to some cell coordinates

    :param cell_coordinates:
        coordinates of cell to calculate adjacent cells coordinates
    :return: adjacent cells coordinates
    :type cell_coordinates: tuple
    :rtype: list
    """

    cells = set()
    x = cell_coordinates[0]
    y = cell_coordinates[1]

    cells.add((x - 1, y))
    cells.add((x + 1, y))

    if y % 2 == 0:
        add_x = 1
    else:
        add_x = -1

    cells.add((x, y - 1))
    cells.add((x + add_x, y - 1))
    cells.add((x, y + 1))
    cells.add((x + add_x, y + 1))

    for coords in list(cells):
        if coords[0] < 0 or coords[0] > 14 or coords[1] < 0 or coords[1] > 10:
            cells.remove(coords)

    return cells

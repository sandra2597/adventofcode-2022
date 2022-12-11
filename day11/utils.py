import collections

def lstring(l):
    new_l = [str(item) for item in l]
    return ";".join(new_l)

def flatten(l):
    return [item for sublist in l for item in sublist]

def forEach(l, function):
    for item in l:
        function(l(item))

def lmap(l, function):
    new_list = []
    for item in l:
        new_list.append(function(item))
    return new_list

def create_default_dict(normal_dict, default_factory):
    new_dict = collections.defaultdict(default_factory)
    for key, value in normal_dict.items():
        new_dict[key] = value
    return new_dict

class Field:
    def __init__(self, row_factory) -> None:
        self.field = []
        self.row_factory = row_factory
        self.max_char_with = 0

    @property
    def size_x(self):
        if len(self.field) == 0:
            return 0
        return len(self.field[0])

    @property
    def size_y(self):
        return len(self.field)

    def create_matrix(self, size_x, size_y, default_value = None):
        self.field = []
        for _ in range(size_y):
            self.field.append([])
            for _ in range(size_x):
                self.field[-1].append(default_value)

    def add_row(self, line):
        self.field.append([])
        for char in line:
            formatted_char = self.row_factory(char)
            self.field[-1].append(formatted_char)
        max_char_width = max(lmap(self.field[-1], lambda x: len(str(x))))
        if max_char_width > self.max_char_with:
            self.max_char_with = max_char_width

    def get_cell(self, x,y):
        if x < 0 or x > self.size_x - 1 or y < 0 or y > self.size_y - 1:
            return None
        return self.field[y][x]

    def set_cell(self, x,y, value):
        self.field[y][x] = value
        if len(str(value)) > self.max_char_with:
            self.max_char_with = len(str(value))
        return value

    def get_relative_cell(self, x, y , dx, dy):
        new_x = x + dx
        new_y = y + dy
        return self.field[len(self.field) - new_y - 1][new_x]

    def print(self, padding_length = None, range_x = None, range_y = None):
        if range_x is None:
            range_x = len(self.field[0])
        if range_y is None:
            range_y = len(self.field)
        if padding_length is None:
            padding_length = self.max_char_with + 1
        for i in range(range_y):
            row = self.field[i]
            string = ''
            for j in range(range_x):
                char = row[j]
                padded_char = str(char).ljust(padding_length, ' ')
                string += padded_char
            print(string)
        print('\n')


    
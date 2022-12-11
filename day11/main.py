from pathlib import Path
from dataclasses import dataclass
import typing

PART = 2

# Reduce worry levels
# Conditions are intact if you subtract a multiple of the divider
# For plus
# x + y % z = 0
# <=> x + y = k * z for a certain k
# <=> for all integers a:
#   x + y - a * z == k * z 
# <=> (x + y - a * z) % z = 0
# For times
# (x + k * z) * c = cx + ck * z
# cx mod z = 0 <=> (cx + kz) mod z = 0
# For quadratic
#(x + k * z) * (x + k * z) = x*x + ( 2*k*x + z ) * z
# x*x mod z = 0 <=> (x + kz)**2 mod z = 0


@dataclass
class Monkey:
    starting_items: list[int]
    operation: typing.Any
    divisible_by: int
    if_test_true: int
    if_test_false: int
    inspected_items: int = 0

    def inspect_items(self, common_divider):
        items_to_remove = []
        self.inspected_items += len(self.starting_items)
        for item in self.starting_items:
            worry_level = self.operation(item)
            if PART == 2:
                worry_level %= common_divider
            if PART == 1:
                worry_level = worry_level // 3
            boolean_value = worry_level % self.divisible_by == 0
            if boolean_value:
                items_to_remove.append({'old_value': item, 'worry_level': worry_level, 'to': self.if_test_true})
            else:
                items_to_remove.append({'old_value': item, 'worry_level': worry_level, 'to': self.if_test_false})
        removed_item_keys = [item['old_value'] for item in items_to_remove]
        self.starting_items = [item for item in self.starting_items if item not in removed_item_keys]
        return items_to_remove

    def add_item(self, worry_level):
        self.starting_items.append(worry_level)
        return

def get_operation(line):
    line = line.replace('  Operation: new = ', '')
    data = line.split(' ')
    operator = data[1]
    second_item = data[2]
    if operator == '*':
        if second_item == 'old':
            operation = lambda x: x * x
        else:
            operation = lambda x: x * int(second_item)
    if operator == '+':
        if second_item == 'old':
            operation = lambda x: x + x
        else:
            operation = lambda x: x + int(second_item)
    return operation

def process_data(data) -> list[Monkey]:
    lines = data.split('\n')
    starting_items = None
    operation = None
    divisible_by = None
    if_test_true = None
    if_test_false = None
    monkeys = []
    for line in lines:
        condition_new_moneky = starting_items is not None and operation is not None and divisible_by is not None and if_test_true is not None and if_test_false is not None
        if condition_new_moneky:
            monkeys.append(Monkey(
                starting_items=starting_items,
                operation=operation,
                divisible_by=divisible_by,
                if_test_true=if_test_true,
                if_test_false=if_test_false,
            ))
            starting_items = None
            operation = None
            divisible_by = None
            if_test_true = None
            if_test_false = None
        if line.startswith('  Starting items: '):
            line = line.replace('  Starting items: ','')
            starting_items = [int(item) for item in line.split(', ')]
            continue
        if line.startswith('  Operation: new = '):
            operation = get_operation(line)

        if line.startswith('  Test: divisible by '):
            line = line.replace('  Test: divisible by ','')
            divisible_by = int(line)
        if line.startswith('    If true: throw to monkey '):
            line = line.replace('    If true: throw to monkey ','')
            if_test_true = int(line)
        if line.startswith('    If false: throw to monkey'):
            line = line.replace('    If false: throw to monkey ','')
            if_test_false = int(line)
    return monkeys
        
        
        

def main():
    path = Path.cwd() / '2022' / 'day11' / 'input.txt'
    with path.open('r') as f:
        data = f.read()
    monkeys = process_data(data)
    common_divider = 1
    for monkey in monkeys:
        common_divider *= monkey.divisible_by
    if PART == 1:
        turns = 20
    else:
        turns = 10000
    for _ in range(turns):
        for monkey in monkeys:
            thrown_items = monkey.inspect_items(common_divider)
            for item in thrown_items:
                worry_level = item['worry_level']
                to = item['to']
                new_monkey = monkeys[to]
                new_monkey.add_item(worry_level)
    inspected_items = [monkey.inspected_items for monkey in monkeys]
    print('inspected_items', inspected_items)
    inspected_items.sort(reverse=True)
    product = inspected_items[0] * inspected_items[1]
    print(product)

if __name__ == '__main__':
    main()
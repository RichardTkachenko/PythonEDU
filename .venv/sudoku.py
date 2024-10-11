import copy, random, sys


EMPTY_SPACE = '.'
GRID_LENGTH = 9
BOX_LENGTH = 3
FULL_GRID_SIZE = GRID_LENGTH * GRID_LENGTH


class SudokuGrid:
    def __init__(self, originalSetup):
        self.originalSetup = originalSetup
        self.grid = {}
        self.resetGrid()
        self.moves = []

    def resetGrid(self):

        for x in range(1, GRID_LENGTH + 1):
            for y in range(1, GRID_LENGTH + 1):
                self.grid[(x, y)] = EMPTY_SPACE

        assert len(self.originalSetup) == FULL_GRID_SIZE
        i = 0
        y = 0
        while i < FULL_GRID_SIZE:
            for x in range(GRID_LENGTH):
                self.grid[(x, y)] = self.originalSetup[i]
                i += 1
            y += 1

    def makeMove(self, column, row, number):

        x = 'ABCDEFGHI'.find(column)
        y = int(row) - 1

        if self.originalSetup[y * GRID_LENGTH + x] != EMPTY_SPACE:
            return False

        self.grid[(x, y)] = number
        self.moves.append(copy.copy(self.grid))
        return True

    def undo(self):
        if self.moves == []:
            return

        self.moves.pop()

        if self.moves == []:
            self.resetGrid()
        else:
            self.grid = copy.copy(self.moves[-1])

    def display(self):
        print('   A B C   D E F   G H I')
        for y in range(GRID_LENGTH):
            for x in range(GRID_LENGTH):
                if x == 0:
                    print(str(y + 1) + '  ', end='')

                print(self.grid[(x, y)] + ' ', end='')
                if x == 2 or x == 5:
                    print('| ', end='')
            print()

            if y == 2 or y == 5:
                print('   ------+-------+------')

    def _isCompleteSetOfNumbers(self, numbers):
        return sorted(numbers) == list('123456789')

    def isSolved(self):
        for row in range(GRID_LENGTH):
            rowNumbers = []
            for x in range(GRID_LENGTH):
                number = self.grid[(x, row)]
                rowNumbers.append(number)
            if not self._isCompleteSetOfNumbers(rowNumbers):
                return False

        for column in range(GRID_LENGTH):
            columnNumbers = []
            for y in range(GRID_LENGTH):
                number = self.grid[(column, y)]
                columnNumbers.append(number)
            if not self._isCompleteSetOfNumbers(columnNumbers):
                return False

        for boxx in (0, 3, 6):
            for boxy in (0, 3, 6):
                boxNumbers = []
                for x in range(BOX_LENGTH):
                    for y in range(BOX_LENGTH):
                        number = self.grid[(boxx + x, boxy + y)]
                        boxNumbers.append(number)
                if not self._isCompleteSetOfNumbers(boxNumbers):
                    return False

        return True


print('''Sudoku Puzzle, by Al Sweigart al@inventwithpython.com

Sudoku is a number placement logic puzzle game. A Sudoku grid is a 9x9
grid of numbers. Try to place numbers in the grid such that every row,
column, and 3x3 box has the numbers 1 through 9 once and only once.

For example, here is a starting Sudoku grid and its solved form:

    5 3 . | . 7 . | . . .     5 3 4 | 6 7 8 | 9 1 2
    6 . . | 1 9 5 | . . .     6 7 2 | 1 9 5 | 3 4 8
    . 9 8 | . . . | . 6 .     1 9 8 | 3 4 2 | 5 6 7
    ------+-------+------     ------+-------+------
    8 . . | . 6 . | . . 3     8 5 9 | 7 6 1 | 4 2 3
    4 . . | 8 . 3 | . . 1 --> 4 2 6 | 8 5 3 | 7 9 1
    7 . . | . 2 . | . . 6     7 1 3 | 9 2 4 | 8 5 6
    ------+-------+------     ------+-------+------
    . 6 . | . . . | 2 8 .     9 6 1 | 5 3 7 | 2 8 4
    . . . | 4 1 9 | . . 5     2 8 7 | 4 1 9 | 6 3 5
    . . . | . 8 . | . 7 9     3 4 5 | 2 8 6 | 1 7 9
''')
input('Press Enter to begin...')


with open('sudokupuzzles.txt') as puzzleFile:
    puzzles = puzzleFile.readlines()

for i, puzzle in enumerate(puzzles):
    puzzles[i] = puzzle.strip()

grid = SudokuGrid(random.choice(puzzles))

while True:
    grid.display()

    if grid.isSolved():
        print('Congratulations! You solved the puzzle!')
        print('Thanks for playing!')
        sys.exit()

    while True:
        print()
        print('Enter a move, or RESET, NEW, UNDO, ORIGINAL, or QUIT:')
        print('(For example, a move looks like "B4 9".)')

        action = input('> ').upper().strip()

        if len(action) > 0 and action[0] in ('R', 'N', 'U', 'O', 'Q'):
            break

        if len(action.split()) == 2:
            space, number = action.split()
            if len(space) != 2:
                continue

            column, row = space
            if column not in list('ABCDEFGHI'):
                print('There is no column', column)
                continue
            if not row.isdecimal() or not (1 <= int(row) <= 9):
                print('There is no row', row)
                continue
            if not (1 <= int(number) <= 9):
                print('Select a number from 1 to 9, not ', number)
                continue
            break

    print()

    if action.startswith('R'):
        grid.resetGrid()
        continue

    if action.startswith('N'):
        grid = SudokuGrid(random.choice(puzzles))
        continue

    if action.startswith('U'):
        grid.undo()
        continue

    if action.startswith('O'):
        originalGrid = SudokuGrid(grid.originalSetup)
        print('The original grid looked like this:')
        originalGrid.display()
        input('Press Enter to continue...')

    if action.startswith('Q'):
        print('Thanks for playing!')
        sys.exit()

    if grid.makeMove(column, row, number) == False:
        print('You cannot overwrite the original grid\'s numbers.')
        print('Enter ORIGINAL to view the original grid.')
        input('Press Enter to continue...')

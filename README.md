# Usage

`py <obfuscator_1|obfuscator_2|obfuscator_2_and_1> <filename>`

## Options:
    -o --output     output name
    -p --print      print on console

# Examples

*obfuscator 1 is very glitchy

## sample 1 outputs

#### with v1

```python
class _while_cond():
 def __init__(self,cond)->None:self.cond=cond
 def __iter__(self):return self
 def __next__(self):
  if self.cond():
   return True
  raise StopIteration
def _for(iter,_else=0):
 try:
  for _ in iter:pass
  else:
   if _else:_else()
 except RuntimeError:
  if _else:_else()
def _break():
 raise StopIteration()

(IlIIIll11Ill1IllI := ())


def IlllIllII1III1I1l():
    raise StopIteration


(lower := 100)
(upper := 2000)
_for(*(((
(order := len(str(num))), 
(sum := 0), 
(temp := num), 
_for((
(digit := temp % 10), 
(sum := sum + digit ** order), 
(temp := temp // 10)) for _ in _while_cond(lambda : temp > 0)), (
[
print(num)] if num == sum else (),)) for num in range(lower, upper + 1)),))
```

#### with v2

```python
(lIlIIll1I1IlII1I1 := ())


def I1l11IIIIl1llI1l1():
    raise StopIteration


lower = 100
upper = 2000
for num in range(lower, upper + 1):
    order = len(str(num))
    sum = 0
    temp = num
    while temp > 0:
        digit = temp % 10
        sum += digit ** order
        temp //= 10
    if num == sum:
        print(*(num,))
```

## sample 2 outputs

#### with v1

```python
class _while_cond():
 def __init__(self,cond)->None:self.cond=cond
 def __iter__(self):return self
 def __next__(self):
  if self.cond():
   return True
  raise StopIteration
def _for(iter,_else=0):
 try:
  for _ in iter:pass
  else:
   if _else:_else()
 except RuntimeError:
  if _else:_else()
def _break():
 raise StopIteration()

"""The n queens puzzle.

https://github.com/sol-prog/N-Queens-Puzzle/blob/master/nqueens.py
"""
(__all__ := [])


class NQueens:
    """Generate all valid solutions for the n queens puzzle"""

    def __init__(self, size):
        self.__size = size
        self.__solutions = 0
        self.__solve()

    def __solve(self):
        """Solve the n queens puzzle and print the number of solutions"""
        positions = [-1] * self.__size
        self.__put_queen(positions, 0)
        print('Found', self.__solutions, 'solutions.')

    def __put_queen(self, positions, target_row):
        """
        Try to place a queen on target_row by checking all N possible cases.
        If a valid place is found the function calls itself trying to place a queen
        on the next row until all N queens are placed on the NxN board.
        """
        if target_row == self.__size:
            self.__show_full_board(positions)
            self.__solutions += 1
        else:
            for column in range(self.__size):
                if self.__check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.__put_queen(positions, target_row + 1)

    def __check_place(self, positions, ocuppied_rows, column):
        """
        Check if a given position is under attack from any of
        the previously placed queens (check column and diagonal positions)
        """
        for i in range(ocuppied_rows):
            if positions[i] == column or positions[i
                ] - i == column - ocuppied_rows or positions[i
                ] + i == column + ocuppied_rows:
                return False
        return True

    def __show_full_board(self, positions):
        """Show the full NxN board"""
        for row in range(self.__size):
            line = ''
            for column in range(self.__size):
                if positions[row] == column:
                    line += 'Q '
                else:
                    line += '. '
            print(line)
        print('\n')

    def __show_short_board(self, positions):
        """
        Show the queens positions on the board in compressed form,
        each number represent the occupied column position in the corresponding row.
        """
        line = ''
        for i in range(self.__size):
            line += str(positions[i]) + ' '
        print(line)


def main():
    """Initialize and solve the n queens puzzle"""
    NQueens(8)


(
[
main()] if __name__ == '__main__' else (),)
```

#### with v2

```python
(l1IIllllll1llIlIl := (bytes((84, 104, 101, 32, 110, 32, 113, 117, 101, 101,
    110, 115, 32, 112, 117, 122, 122, 108, 101, 46, 10, 10, 104, 116, 116, 
    112, 115, 58, 47, 47, 103, 105, 116, 104, 117, 98, 46, 99, 111, 109, 47,
    115, 111, 108, 45, 112, 114, 111, 103, 47, 78, 45, 81, 117, 101, 101, 
    110, 115, 45, 80, 117, 122, 122, 108, 101, 47, 98, 108, 111, 98, 47, 
    109, 97, 115, 116, 101, 114, 47, 110, 113, 117, 101, 101, 110, 115, 46,
    112, 121, 10)).decode(), bytes((71, 101, 110, 101, 114, 97, 116, 101, 
    32, 97, 108, 108, 32, 118, 97, 108, 105, 100, 32, 115, 111, 108, 117, 
    116, 105, 111, 110, 115, 32, 102, 111, 114, 32, 116, 104, 101, 32, 110,
    32, 113, 117, 101, 101, 110, 115, 32, 112, 117, 122, 122, 108, 101)).
    decode(), bytes((83, 111, 108, 118, 101, 32, 116, 104, 101, 32, 110, 32,
    113, 117, 101, 101, 110, 115, 32, 112, 117, 122, 122, 108, 101, 32, 97,
    110, 100, 32, 112, 114, 105, 110, 116, 32, 116, 104, 101, 32, 110, 117,
    109, 98, 101, 114, 32, 111, 102, 32, 115, 111, 108, 117, 116, 105, 111,
    110, 115)).decode(), bytes((70, 111, 117, 110, 100)).decode(), bytes((
    115, 111, 108, 117, 116, 105, 111, 110, 115, 46)).decode(), bytes((10, 
    32, 32, 32, 32, 32, 32, 32, 32, 84, 114, 121, 32, 116, 111, 32, 112, 
    108, 97, 99, 101, 32, 97, 32, 113, 117, 101, 101, 110, 32, 111, 110, 32,
    116, 97, 114, 103, 101, 116, 95, 114, 111, 119, 32, 98, 121, 32, 99, 
    104, 101, 99, 107, 105, 110, 103, 32, 97, 108, 108, 32, 78, 32, 112, 
    111, 115, 115, 105, 98, 108, 101, 32, 99, 97, 115, 101, 115, 46, 10, 32,
    32, 32, 32, 32, 32, 32, 32, 73, 102, 32, 97, 32, 118, 97, 108, 105, 100,
    32, 112, 108, 97, 99, 101, 32, 105, 115, 32, 102, 111, 117, 110, 100, 
    32, 116, 104, 101, 32, 102, 117, 110, 99, 116, 105, 111, 110, 32, 99, 
    97, 108, 108, 115, 32, 105, 116, 115, 101, 108, 102, 32, 116, 114, 121,
    105, 110, 103, 32, 116, 111, 32, 112, 108, 97, 99, 101, 32, 97, 32, 113,
    117, 101, 101, 110, 10, 32, 32, 32, 32, 32, 32, 32, 32, 111, 110, 32, 
    116, 104, 101, 32, 110, 101, 120, 116, 32, 114, 111, 119, 32, 117, 110,
    116, 105, 108, 32, 97, 108, 108, 32, 78, 32, 113, 117, 101, 101, 110, 
    115, 32, 97, 114, 101, 32, 112, 108, 97, 99, 101, 100, 32, 111, 110, 32,
    116, 104, 101, 32, 78, 120, 78, 32, 98, 111, 97, 114, 100, 46, 10, 32, 
    32, 32, 32, 32, 32, 32, 32)).decode(), bytes((10, 32, 32, 32, 32, 32, 
    32, 32, 32, 67, 104, 101, 99, 107, 32, 105, 102, 32, 97, 32, 103, 105, 
    118, 101, 110, 32, 112, 111, 115, 105, 116, 105, 111, 110, 32, 105, 115,
    32, 117, 110, 100, 101, 114, 32, 97, 116, 116, 97, 99, 107, 32, 102, 
    114, 111, 109, 32, 97, 110, 121, 32, 111, 102, 10, 32, 32, 32, 32, 32, 
    32, 32, 32, 116, 104, 101, 32, 112, 114, 101, 118, 105, 111, 117, 115, 
    108, 121, 32, 112, 108, 97, 99, 101, 100, 32, 113, 117, 101, 101, 110, 
    115, 32, 40, 99, 104, 101, 99, 107, 32, 99, 111, 108, 117, 109, 110, 32,
    97, 110, 100, 32, 100, 105, 97, 103, 111, 110, 97, 108, 32, 112, 111, 
    115, 105, 116, 105, 111, 110, 115, 41, 10, 32, 32, 32, 32, 32, 32, 32, 
    32)).decode(), bytes((83, 104, 111, 119, 32, 116, 104, 101, 32, 102, 
    117, 108, 108, 32, 78, 120, 78, 32, 98, 111, 97, 114, 100)).decode(),
    bytes((10,)).decode(), bytes((10, 32, 32, 32, 32, 32, 32, 32, 32, 83, 
    104, 111, 119, 32, 116, 104, 101, 32, 113, 117, 101, 101, 110, 115, 32,
    112, 111, 115, 105, 116, 105, 111, 110, 115, 32, 111, 110, 32, 116, 104,
    101, 32, 98, 111, 97, 114, 100, 32, 105, 110, 32, 99, 111, 109, 112, 
    114, 101, 115, 115, 101, 100, 32, 102, 111, 114, 109, 44, 10, 32, 32, 
    32, 32, 32, 32, 32, 32, 101, 97, 99, 104, 32, 110, 117, 109, 98, 101, 
    114, 32, 114, 101, 112, 114, 101, 115, 101, 110, 116, 32, 116, 104, 101,
    32, 111, 99, 99, 117, 112, 105, 101, 100, 32, 99, 111, 108, 117, 109, 
    110, 32, 112, 111, 115, 105, 116, 105, 111, 110, 32, 105, 110, 32, 116,
    104, 101, 32, 99, 111, 114, 114, 101, 115, 112, 111, 110, 100, 105, 110,
    103, 32, 114, 111, 119, 46, 10, 32, 32, 32, 32, 32, 32, 32, 32)).decode
    (), bytes((73, 110, 105, 116, 105, 97, 108, 105, 122, 101, 32, 97, 110,
    100, 32, 115, 111, 108, 118, 101, 32, 116, 104, 101, 32, 110, 32, 113, 
    117, 101, 101, 110, 115, 32, 112, 117, 122, 122, 108, 101)).decode(),
    bytes((95, 95, 109, 97, 105, 110, 95, 95)).decode()))


def IlI11111l111Il11I():
    raise StopIteration


l1IIllllll1llIlIl[0]
__all__ = []


class NQueens:
    l1IIllllll1llIlIl[1]

    def __init__(self, size):
        self.__size = size
        self.__solutions = 0
        self.__solve(*())

    def __solve(self):
        l1IIllllll1llIlIl[2]
        positions = [-1] * self.__size
        self.__put_queen(*(positions, 0))
        print(*(l1IIllllll1llIlIl[3], self.__solutions, l1IIllllll1llIlIl[4]))

    def __put_queen(self, positions, target_row):
        l1IIllllll1llIlIl[5]
        if target_row == self.__size:
            self.__show_full_board(*(positions,))
            self.__solutions += 1
        else:
            for column in range(self.__size):
                if self.__check_place(positions, target_row, column):
                    positions[target_row] = column
                    self.__put_queen(positions, target_row + 1)

    def __check_place(self, positions, ocuppied_rows, column):
        l1IIllllll1llIlIl[6]
        for i in range(ocuppied_rows):
            if not (not positions[i] == column and not positions[i] - i == 
                column - ocuppied_rows and not positions[i] + i == column +
                ocuppied_rows):
                return False
        return True

    def __show_full_board(self, positions):
        l1IIllllll1llIlIl[7]
        for row in range(self.__size):
            line = ''
            for column in range(self.__size):
                if positions[row] == column:
                    line += 'Q '
                else:
                    line += '. '
            print(*(line,))
        print(*(l1IIllllll1llIlIl[8],))

    def __show_short_board(self, positions):
        l1IIllllll1llIlIl[9]
        line = ''
        for i in range(self.__size):
            line += str(positions[i]) + ' '
        print(*(line,))


def main():
    l1IIllllll1llIlIl[10]
    NQueens(*(8,))


if __name__ == l1IIllllll1llIlIl[11]:
    main(*())
```

class Link:
    """A linked list.

    >>> s = Link(3, Link(4, Link(5)))
    >>> s
    Link(3, Link(4, Link(5)))
    >>> print(s)
    <3 4 5>
    >>> s.first
    3
    >>> s.rest
    Link(4, Link(5))
    >>> s.rest.first
    4
    >>> s.rest.first = 7
    >>> s
    Link(3, Link(7, Link(5)))
    >>> s.first = 6
    >>> s.rest.rest = Link.empty
    >>> s
    Link(6, Link(7))
    >>> print(s.rest)
    <7>
    >>> t = Link(1, Link(Link(2, Link(3)), Link(4)))
    >>> t
    Link(1, Link(Link(2, Link(3)), Link(4)))
    >>> print(t)
    <1 <2 3> 4>

    >>> s.second
    7
    >>> s.second = 8
    >>> print(s)
    <6 8>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

    @property # 输入second不加括号，就会输出结果
    def second(self):
        return self.rest.first

    @second.setter # 对应于second函数，可以改变数值
    def second(self, value):
        self.rest.first = value

# Efficiency

def fib(n):
    """The nth Fibonacci number.

    >>> fib(20)
    6765
    """
    if n == 0 or n == 1:
        return n
    else:
        return fib(n-2) + fib(n-1)

# Time

def count(f):
    """Return a counted version of f with a call_count attribute.

    >>> def fib(n):
    ...     if n == 0 or n == 1:
    ...         return n
    ...     else:
    ...         return fib(n-2) + fib(n-1)
    >>> fib = count(fib)
    >>> fib(20)
    6765
    >>> fib.call_count
    21891
    """
    def counted(*args):
        counted.call_count += 1
        return f(*args)
    counted.call_count = 0
    return counted

# Memoization

def memo(f):
    """Memoize f.

    >>> def fib(n):
    ...     if n == 0 or n == 1:
    ...         return n
    ...     else:
    ...         return fib(n-2) + fib(n-1)
    >>> fib = count(fib)
    >>> fib(20)
    6765
    >>> fib.call_count
    21891
    >>> counted_fib = count(fib)
    >>> fib  = memo(counted_fib)
    >>> fib(20)
    6765
    >>> counted_fib.call_count
    21
    >>> fib(35)
    9227465
    >>> counted_fib.call_count
    36
    """
    cache = {}
    def memoized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memoized

# Trees

class Tree:
    """A tree is a label and a list of branches."""
    def __init__(self, label, branches=[]):
        self.label = label
        for branch in branches:
            assert isinstance(branch, Tree)
        self.branches = list(branches)

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(repr(self.label), branch_str)

    def __str__(self):
        return '\n'.join(self.indented())

    def indented(self):
        lines = []
        for b in self.branches:
            for line in b.indented():
                lines.append('  ' + line)
        return [str(self.label)] + lines

    def is_leaf(self):
        return not self.branches

@memo # 这里使用的是装饰器，作用就是现在的fib_tree = memo(fib_tree),memo会将fib_tree每次的结果记录下来
def fib_tree(n):
    """A Fibonacci tree.

    >>> print(fib_tree(4))
    3
      1
        0
        1
      2
        1
        1
          0
          1
    """
    if n == 0 or n == 1:
        return Tree(n)
    else:
        left = fib_tree(n-2)
        right = fib_tree(n-1)
        fib_n = left.label + right.label
        return Tree(fib_n, [left, right])

def leaves(tree):
    """Return the leaf values of a tree.

    >>> leaves(fib_tree(4))
    [0, 1, 1, 0, 1]
    """
    if tree.is_leaf():
        return [tree.label]
    else:
        return sum([leaves(b) for b in tree.branches], [])

def height(tree):
    """The height of a tree."""
    if tree.is_leaf():
        return 0
    else:
        return 1 + max([height(b) for b in tree.branches])

def prune(t, n):
    """Prune sub-trees whose label value is n.

    >>> t = fib_tree(5)
    >>> prune(t, 1)
    >>> print(t)
    5
      2
      3
        2
    """
    t.branches = [b for b in t.branches if b.label != n]
    for b in t.branches:
        prune(b, n)

def prune_repeats(t, seen):
    """Remove repeated sub-trees

    >>> def fib_tree(n):
    ...     if n == 0 or n == 1:
    ...         return Tree(n)
    ...     else:
    ...         left = fib_tree(n-2)
    ...         right = fib_tree(n-1)
    ...         return Tree(left.label + right.label, (left, right))
    >>> fib_tree = memo(fib_tree)
    >>> t = fib_tree(6)
    >>> print(t)
    8
      3
        1
          0
          1
        2
          1
          1
            0
            1
      5
        2
          1
          1
            0
            1
        3
          1
            0
            1
          2
            1
            1
              0
              1
    >>> prune_repeats(t, [])
    >>> print(t)
    8
      3
        1
          0
          1
        2
      5
    """
    t.branches = [b for b in t.branches if b not in seen]
    seen.append(t)
    for b in t.branches:
        prune_repeats(b, seen)


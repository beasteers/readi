import readi


def test_register():
    col = readi.Collection()

    @col.register
    def asdf():
        pass

    @col.register
    def asdf1():
        pass

    def asdf2():
        pass
    col.register(asdf2, 'asdf3')

    @col.register('asdf5')
    def asdf4():
        pass

    assert set(col) == {'asdf', 'asdf1', 'asdf3', 'asdf5'}


def test_gather():
    col = readi.Collection()

    @col.register
    def asdf(**kw):
        return {'i': 1, **kw}

    @col.register
    def asdf1(**kw):
        return {'i': 2, **kw}

    assert col.gather() == [{'i': 1}, {'i': 2}]
    assert col.gather(a=5) == [{'i': 1, 'a': 5}, {'i': 2, 'a': 5}]
    assert col.gather(asdf1=False, a=5, b=6) == [{'i': 1, 'a': 5, 'b': 6}]
    assert col.gather('asdf', a=5) == [{'i': 1, 'a': 5}]


def test_subclass():
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    col = readi.Collection()
    col.register_subclasses(A)
    assert set(col) == {'b', 'c'}

    col.clear()
    col.register_subclasses(A, include=True)
    assert set(col) == {'a', 'b', 'c'}

    class D(A):
        pass
    col.refresh_subclasses()
    assert set(col) == {'a', 'b', 'c', 'd'}

def test_functions():
    col = readi.Collection()

    @col.register
    def a():
        return 5

    @col.register
    def b():
        return 6

    assert set(col) == {'a', 'b'}
    assert set(col.gather()) == {5, 6}
    assert col.getone('a') == 5

def test_function_closure():
    col = readi.Collection()
    @col.register
    def a(x=7):
        return lambda: x

    @col.register
    def b(x=7):
        return lambda: x * 2

    assert set(f() for f in col.gather(x=9)) == {9, 18}

def test_function_wrap():
    col = readi.Collection()
    @col.register
    @readi.wrap
    def a(x=7):
        return x

    @col.register
    @readi.wrap
    def b(x=7):
        return x * 2

    assert set(f() for f in col.gather(x=9)) == {9, 18}

def test_variants():
    col = readi.Collection()

    @col.register
    def a(**kw):
        return {**kw}

    assert col.gather() == [{}]
    col.register_variant('a', x=7)
    assert set(col) == {'a'}

    col.register_variant('a', 'b', x=8)
    assert set(col) == {'a', 'b'}

    assert col.gather() == [{'x': 7}, {'x': 8}]
    assert col.gather(x=9) == [{'x': 9}, {'x': 9}]

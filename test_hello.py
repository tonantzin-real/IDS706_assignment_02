from hello import say_hello, add, another_function


def test_say_hello():
    assert (
        say_hello("Annie")
        == "Hello, Annie, welcome to Data Engineering Systems (IDS 706)!"
    )


def test_add():
    assert add(2, 3) == 5


def test_another_function():
    assert another_function(2, 3.0) == 6.0

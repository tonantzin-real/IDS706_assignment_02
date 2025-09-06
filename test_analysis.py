import IDS706_assignment_02.utils 


def test_say_hello():
    assert (
        say_hello("Annie")
        == "Hello, Annie, welcome to Data Engineering Systems (IDS 706)!"
    )


def test_add():
    assert add(2, 3) == 5


def test_another_function():
    assert another_function(2, 3.0) == 6.0

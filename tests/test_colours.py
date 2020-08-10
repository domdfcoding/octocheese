# this package
from octocheese import colours


def test_success(capsys):
	colours.success("hello world")

	captured = capsys.readouterr()
	assert captured.out == "\033[32mhello world\033[39m\n"

	colours.success("hello world")
	colours.success("something else")

	captured = capsys.readouterr()
	assert captured.out == "\033[32mhello world\033[39m\n\033[32msomething else\033[39m\n"

	colours.success(1234)

	captured = capsys.readouterr()
	assert captured.out == "\033[32m1234\033[39m\n"


def test_warning(capsys):
	colours.warning("hello world")

	captured = capsys.readouterr()
	assert captured.err == "\033[33mhello world\033[39m\n"

	colours.warning("hello world")
	colours.warning("something else")

	captured = capsys.readouterr()
	assert captured.err == "\033[33mhello world\033[39m\n\033[33msomething else\033[39m\n"

	colours.warning(1234)

	captured = capsys.readouterr()
	assert captured.err == "\033[33m1234\033[39m\n"


def test_error(capsys):
	colours.error("hello world")

	captured = capsys.readouterr()
	assert captured.err == "\033[31mhello world\033[39m\n"

	colours.error("hello world")
	colours.error("something else")

	captured = capsys.readouterr()
	assert captured.err == "\033[31mhello world\033[39m\n\033[31msomething else\033[39m\n"

	colours.error(1234)

	captured = capsys.readouterr()
	assert captured.err == "\033[31m1234\033[39m\n"

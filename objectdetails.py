"""
This module provides function to get Object introspection details
"""
import inspect
import reprlib
import itertools

DEFAULT_LENGTH = 140


class Customer():
    """
    Sample class to test print_object_details function
    """
    def __init__(self, first_name: str, last_name: str, age: int, gender: str):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

    def get_full_name(self):
        """
        Return full customer's name
        """
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return 'Customer'


def print_table(rows, *column_headers) -> None:
    """
    Print data in a table format
    """
    num_of_columns = len(rows[0])
    num_of_headers = len(column_headers)
    if num_of_headers != num_of_columns:
        raise TypeError(f"Expected {num_of_columns} column_headers arguments, "
                        f"got {num_of_headers}.")

    rows_with_headers = itertools.chain([column_headers], rows)
    columns_of_rows = list(zip(*rows_with_headers))
    column_widths = [max(map(len, column)) for column in columns_of_rows]
    column_specs = (f'{{:{w}}}' for w in column_widths)
    format_spec = ' '.join(column_specs)
    print(format_spec.format(*column_headers))
    rules = ('-' * width for width in column_widths)
    print(format_spec.format(*rules))

    for row in rows:
        print(format_spec.format(*row))


def full_signature(method: object) -> str:
    """
    Return full signature of an object
    """
    try:
        return method.__name__ + " " + str(inspect.signature(method))
    except ValueError:
        return method.__name__ + ' (...)'


def brief_documentation(method: object) -> str:
    """
    Return first line of an object documentation
    """
    doc = method.__doc__
    if doc is not None:
        lines = doc.splitlines()
        if len(lines) > 0:
            return lines[0]
    return ''


def print_section_delimiter(length=DEFAULT_LENGTH) -> None:
    """
    Print delimiter as a line between sections
    """
    print('='*length)


def print_type(obj: object) -> None:
    """
    Print type of an object
    """
    print(f'{type(obj)}')


def print_documentation(obj: object) -> None:
    """
    Print docs of an object
    """
    print(inspect.getdoc(obj))


def print_attributes(obj: object) -> None:
    """
    Print docs of an object
    """
    all_attributes = set(dir(obj))
    names_of_methods = set(
        filter(lambda atrr_name: callable(getattr(obj, atrr_name)), all_attributes)
        )
    attributes_excluding_methods = all_attributes - names_of_methods
    attributes_names_and_values = [(name, reprlib.repr(getattr(obj, name)))
                                   for name in attributes_excluding_methods]
    print_table(attributes_names_and_values, "Name", "Value")


def print_methods(obj: object) -> None:
    """
    Print methods of an object
    """
    all_attributes = set(dir(obj))
    names_of_methods = set(
        filter(lambda atrr_name: callable(getattr(obj, atrr_name)), all_attributes)
        )
    methods = (getattr(obj, method_name) for method_name in names_of_methods)
    methods_names_and_docs = [(full_signature(method), brief_documentation(method))
                              for method in methods]
    print_table(methods_names_and_docs, "Name", "Description")


def print_section(obj: object, section_name: str, function_name: object) -> None:
    """
    Print Section details
    """
    print_section_delimiter()
    print(f'{section_name}:\n')
    function_name(obj)


def print_title(obj: object) -> None:
    """
    Print title for an object output
    """
    title = f'Object "{obj.__str__()}" details'
    num_of_fill_symbols = (DEFAULT_LENGTH - 4 - len(title)) // 2
    full_title = f"{'#'*num_of_fill_symbols}  {title}  {'#'*num_of_fill_symbols}"
    if len(full_title) < DEFAULT_LENGTH:
        full_title += '#'*(DEFAULT_LENGTH - len(full_title))
    print(full_title)


def print_object_details(obj: object) -> None:
    """
    Print object introspection details
    """
    print_section(obj, 'Type', print_type)
    print_section(obj, 'Documentation', print_documentation)
    print_section(obj, 'Attributes', print_attributes)
    print_section(obj, 'Methods', print_methods)
    print_section_delimiter()


def main():
    """
    Test printing obect details
    """
    test_customer = Customer('Jake', 'Robin', 25, 'Male')

    print_title(test_customer)
    print_object_details(test_customer)


if __name__ == '__main__':
    main()

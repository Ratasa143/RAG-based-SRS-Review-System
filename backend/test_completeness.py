from core.completeness_checker import check_completeness

requirement = """
The librarian shall issue books to registered students.
"""

result = check_completeness(requirement)

print(result)
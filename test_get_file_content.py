from functions.get_file_content import get_file_content
from config import MAX_CHARS

content =  get_file_content("calculator", "lorem.txt")
content_length = len(content)

if content_length > MAX_CHARS:
    print(f"Success! Received {content_length} characters.")
else:
    print(f"Something is wrong. Only received {content_length} characters.")

expected_msg = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'

if content.endswith(expected_msg):
    print("Test passed! Lorem.txt was truncated correctly.")
else:
    print("Test failed! Expected truncation message was not found.")

print("Result for 'main.py' file:")
print(get_file_content("calculator", "main.py"))

print("Result for 'pkg/calculator.py' file:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Result for '/bin/cat' file:")
print(get_file_content("calculator", "/bin/cat"))

print("Result for 'pkg/does_not_exist.py' file:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))

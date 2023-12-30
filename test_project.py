import project
from save import SaveFile
import pytest

def test_password():
    file = SaveFile("Rei")
    project.match_password(file, "hello")
    assert project.validate_password(file, "hello") == True
    assert project.validate_password(file, "hadhas") == False
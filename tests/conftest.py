# tests/conftest.py
import pytest

class DummyBolt:
    def __init__(self, diameter):
        self.diameter = diameter

class DummyMember:
    def __init__(self, web_thickness=10, flange_thickness=20, depth=300, flange_width=150, r1=5):
        self.web_thickness = web_thickness
        self.flange_thickness = flange_thickness
        self.depth = depth
        self.flange_width = flange_width
        self.r1 = r1

class DummyPlate:
    def __init__(self, thickness, height):
        self.thickness = thickness
        self.height = height

@pytest.fixture
def bolt():
    return DummyBolt(diameter=20)

@pytest.fixture
def supported_member():
    return DummyMember(web_thickness=12, flange_thickness=18, depth=300, flange_width=180, r1=6)

@pytest.fixture
def supporting_member():
    return DummyMember(web_thickness=10, flange_thickness=15, depth=310, flange_width=190, r1=5)

@pytest.fixture
def plate():
    return DummyPlate(thickness=10, height=120)

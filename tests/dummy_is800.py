# tests/dummy_is800.py
class FakeIS800:
    @staticmethod
    def cl_10_5_2_3_min_weld_size(p1, p2):
        return 2

    @staticmethod
    def cl_10_5_3_1_max_weld_throat_thickness(p1, p2):
        return 4

IS800_2007 = FakeIS800()

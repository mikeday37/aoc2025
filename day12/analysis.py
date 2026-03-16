from common import *
from enum import StrEnum
from .solve import *

_shapes, _regions = parse_input(read_input())

def are_all_shapes_3x3():
    return all(s.def_width == 3 and s.def_height == 3 for s in _shapes)
    
test(are_all_shapes_3x3, True)

print("Region Count:", len(_regions))

def calc_total_presents_area(shapes: tuple[Shape, ...], region: Region):
    return sum(shapes[i].area * n for i, n in enumerate(region.presents))

class RegionStatus(StrEnum):
    Unknown = "Unknown"
    Possible = "Possible"
    Impossible = "Impossible"

class RegionInfo:
    region: Region
    area: int
    presents_area: int # total number of cells taken up by the required presents
    status: RegionStatus

    def __init__(self, region: Region):
        self.region = region
        self.area = region.width * region.height
        self.presents_count = sum(region.presents)
        self.presents_area = calc_total_presents_area(_shapes, region)
        if self.presents_area > self.area:
            self.status = RegionStatus.Impossible
        elif (region.width // 3) * (region.height // 3) >= self.presents_count:
            self.status = RegionStatus.Possible
        else:
            self.status = RegionStatus.Unknown

_region_info = list(map(RegionInfo, _regions))

_region_counts = {
        str(status): sum(1 for ri in _region_info if ri.status == status)
        for status in [RegionStatus.Unknown, RegionStatus.Possible, RegionStatus.Impossible]
    }

print("Region Counts:", _region_counts)

def check_already_have_answer():
    return _region_counts[str(RegionStatus.Unknown)] == 0

test(check_already_have_answer, True)

def get_puzzle_answer():
    return _region_counts[str(RegionStatus.Possible)] if check_already_have_answer else None

verify_known_answer(get_puzzle_answer, 534)

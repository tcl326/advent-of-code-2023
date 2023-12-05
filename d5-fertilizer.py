from typing import Tuple, List, Optional

class RangeMap(object):
    def __init__(self):
        self.sources = []
        self.destinations = []
        self.lengths = []
    
    def __getitem__(self, key: int):
        for i, s in enumerate(self.sources):
            if s <= key and s + self.lengths[i] > key:
                return self.destinations[i] + key - s
        return key
    
    def _map_range_single(self, start: int, length: int, r_start: int, r_dest: int, r_length: int) -> Optional[Tuple[int, int, int]]:
        end = start + length
        r_end = r_start + r_length
        # check if the ranges overlaps
        if r_start >= end or start >= r_end:
            # range do not overlap
            return None
        if r_end > start and start >= r_start and end >= r_end:
            return start, start - r_start + r_dest, r_end - start
        if end > r_start and r_end >= end and r_start >= start:
            return r_start, r_dest, end - r_start
        if end >= r_end and start <= r_start:
            return r_start, r_dest, r_length
        if r_end >= end and r_start <= start:
            return start, r_dest + start - r_start, length
        raise ValueError("you shouldn't have been able to reach this place!!!!")


    def map_range(self, start: int, length: int) -> List[List[int]]:
        mapped_range = []
        source_range = []
        for i, source in enumerate(self.sources):
            v = self._map_range_single(start, length, source, self.destinations[i], self.lengths[i])
            if not v:
                continue
            s, d, l = v
            # print(start, length, source, self.destinations[i], self.lengths[i], v)
            mapped_range.append((d, l))
            source_range.append((s, l))
        
        source_range.sort()
        c_start = start
        for (s, l) in source_range:
            if c_start < s:
                mapped_range.append((c_start, s - c_start))
            c_start = s + l
        if c_start < start + length:
            mapped_range.append((c_start, start + length - c_start))
        return sorted(mapped_range)


    
    def add_range(self, source: int, destination: int, length: int):
        self.sources.append(source)
        self.destinations.append(destination)
        self.lengths.append(length)

    def __repr__(self):
        return str([self.sources, self.destinations, self.lengths])


def parse_seeds(line: str) -> List[int]:
    assert line.startswith("seeds:")
    seeds = [int(s) for s in line[len("seeds: "):].split()]
    return seeds

def parse_map(line: str) -> Tuple[str, str]:
    assert "map:" in line
    mapping, _ = line.split()
    source, _, dest = mapping.split("-")
    return source, dest


def parse_range(line: str) -> Tuple[int, int, int]:
    source, destination, length = line.strip().split()
    return int(source), int(destination), int(length)


def get_location(seed, maps):
    s = seed
    for (dest, source), map in maps.items():
        print(seed, dest, s, source, map[s])
        s = map[s]
    return s


def part1(seeds, maps):
    min_loc = float('inf')
    for seed in seeds:
        min_loc = min(min_loc, get_location(seed, maps))
    return min_loc

def part2(seeds, maps):
    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for (dest, source), map in maps.items():
        next_seeds = []
        for start, length in seeds:
            print(dest, source, (start, length), map.map_range(start, length))
            next_seeds.extend(map.map_range(start, length))
        seeds = next_seeds
    next_seeds.sort()
    return next_seeds[0][0]


if __name__ == "__main__":
    file_name = "d5-input.text"

    maps = {}

    with open(file_name, "r") as f:
        seeds = parse_seeds(f.readline())

        line = f.readline()
        while line:
            line = line.strip()
            if not line:
                pass
            elif "map:" in line:
                source_name, dest_name = parse_map(line)
                r_map = RangeMap()
                maps[(source_name, dest_name)] = r_map
            else:
                d, s, r = parse_range(line)
                r_map.add_range(s, d, r)
            line = f.readline()
    # print(maps)
    print(part1(seeds, maps))
    print(part2(seeds, maps))

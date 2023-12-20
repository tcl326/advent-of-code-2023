
from typing import Tuple, List, Dict, Optional
import tqdm
import math
import collections
from enum import Enum


class ModuleType(Enum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCAST = "broadcaster"


class Module:
    def __init__(self, dest: List[str]):
        self.dest = dest
        self.inputs: List[str] = []
    
    def add_input(self, module: str):
        self.inputs.append(module)

    def pulse(self, p: int, input: str) -> Tuple[int, List[str]]:
        pass

    def __repr__(self) -> str:
        return f"dest: {self.dest}, inputs: {self.inputs}"


class FlipFlopModule(Module):
    def __init__(self, dest: List[str]):
        super().__init__(dest)
        self.is_on = False
    
    def pulse(self, p: int, input: str) -> Tuple[int, List[str]]:
        if p == 1:
            return 0, []
        self.is_on = not self.is_on
        return int(self.is_on), self.dest

    def __repr__(self) -> str:
        return f"Flip-Flop({super().__repr__()})"


class ConjunctionModule(Module):
    def __init__(self, dest: List[str]):
        super().__init__(dest)
        self.most_recent_pulse = {}
    
    def pulse(self, p: int, input: str) -> Tuple[int, List[str]]:
        if not self.most_recent_pulse:
            self.most_recent_pulse = {n: 0 for n in self.inputs}
        
        self.most_recent_pulse[input] = p
        if sum(self.most_recent_pulse.values()) == len(self.most_recent_pulse):
            return 0, self.dest
        return 1, self.dest

    def __repr__(self) -> str:
        return f"Conjunction({super().__repr__()}, {self.most_recent_pulse})"


class BroadcastModule(Module):
    def pulse(self, p: int, input: str) -> Tuple[int, List[str]]:
        return p, self.dest

    def __repr__(self) -> str:
        return f"Broadcast({super().__repr__()})"


def create_module(type: ModuleType, dest: List[str]) -> Module:
    if type == ModuleType.BROADCAST:
        return BroadcastModule(dest)
    elif type == ModuleType.FLIP_FLOP:
        return FlipFlopModule(dest)
    return ConjunctionModule(dest)


def parse_module(line: str) -> Tuple[ModuleType, str, List[str]]:
    m, dest = line.split("->")
    m, dest = m.strip(), dest.strip()
    dest = [d.strip() for d in dest.split(",")]
    if m == "broadcaster":
        module = ModuleType.BROADCAST
        name = m
    else:
        if m[0] == ModuleType.FLIP_FLOP.value:
            module = ModuleType.FLIP_FLOP
        else:
            module = ModuleType.CONJUNCTION
        name = m[1:]
    return module, name, dest
            

def part1(modules: Dict[str, Tuple[ModuleType, List[str]]]) -> int:
    module_dict = {
        n: create_module(t, d) for n, (t, d) in modules.items()
    }

    for name, module in module_dict.items():
        for d in module.dest:
            if d in module_dict:
                module_dict[d].add_input(name)
    
    low = 0
    high = 0
    seen = {}
    for i in tqdm.tqdm(range(1, 1_000 + 1)):
        queue = collections.deque([(0, "button", "broadcaster", module_dict["broadcaster"])])
        low += 1
        
        while queue:
            p, prev, k, m = queue.popleft()
            np, dest = m.pulse(p, prev)
            # print(f"{prev} -{p}> {k} -{np}> {dest}", m)
            if np == 0 and "rx" in dest:
                return (i + 1)
            for d in dest:
                if np == 0:
                    low += 1
                else:
                    high += 1
                if d in module_dict:
                    queue.append((np, k, d, module_dict[d]))
    print(module_dict)
    return low * high


def part2(modules: Dict[str, Tuple[ModuleType, List[str]]]) -> int:
    module_dict = {
        n: create_module(t, d) for n, (t, d) in modules.items()
    }

    for name, module in module_dict.items():
        for d in module.dest:
            if d in module_dict:
                module_dict[d].add_input(name)
    
    low = 0
    high = 0
    seen = {}
    for i in tqdm.tqdm(range(1, 1_000_000_000)):
        queue = collections.deque([(0, "button", "broadcaster", module_dict["broadcaster"])])
        low += 1
        
        while queue:
            p, prev, k, m = queue.popleft()
            np, dest = m.pulse(p, prev)
            if isinstance(m, ConjunctionModule) and k in ["fh", "mf", "fz", "ss"] and np:
                print(i, k, dest)
                seen[k] = i
                print(seen)
                if len(seen) == 4:
                    return math.lcm(*seen.values())
            # print(f"{prev} -{p}> {k} -{np}> {dest}", m)
            if np == 0 and "rx" in dest:
                return (i + 1)
            for d in dest:
                if np == 0:
                    low += 1
                else:
                    high += 1
                if d in module_dict:
                    queue.append((np, k, d, module_dict[d]))
    print(module_dict)
    return low * high




if __name__ == "__main__":
    file_name = "d20-input.text"
    # file_name = "test_input.text"
    modules = {}
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            module, name, dest = parse_module(line)
            modules[name] = (module, dest)
            line = f.readline()
    # print(modules)
    print(part1(modules))
    print(part2(modules))
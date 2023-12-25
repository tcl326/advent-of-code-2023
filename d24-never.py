
from typing import List, Tuple, Optional

import numpy as np


def parse_line(line: str):
    position, velocity = line.split("@")
    pos = [int(p) for p in position.strip().split(",")]
    vel = [int(v) for v in velocity.strip().split(",")]
    return pos[0], pos[1], pos[2], vel[0], vel[1], vel[2]


def find_intersect(x1, y1, vx1, vy1, x2, y2, vx2, vy2) -> Optional[Tuple[int, int]]:
    num_t = ((x2 - x1) * vy2 - (y2- y1) * vx2)
    num_u = ((x2 - x1) * vy1 - (y2 - y1) * vx1)
    denum = (vx1 * vy2 - vy1 * vx2)
    if denum == 0 or num_t / denum < 0 or num_u / denum < 0:
        return None
    t = num_t / denum
    return x1 + t * vx1, y1 + t * vy1


def part1(hailstones: List[Tuple[int, int, int, int, int, int]], least: int, most: int) -> int:
    r = 0
    for i in range(len(hailstones)):
        for j in range(i + 1, len(hailstones)):
            if i == j:
                continue
            x1, y1, z1, vx1, vy1, vz1 = hailstones[i]
            x2, y2, z2, vx2, vy2, vz2 = hailstones[j]
            intersect = find_intersect(x1, y1, vx1, vy1, x2, y2, vx2, vy2)
            if intersect:
                xi, yi = intersect
                if xi > least and xi < most and yi > least and yi < most:
                    r += 1
    return r

def part2(hailstones: List[Tuple[int, int, int, int, int, int]]) -> int:
    def cross_matrix(vec):
        return np.array([
            [0, -1 * vec[2], vec[1]],
            [vec[2], 0, -1 * vec[0]],
            [-1 * vec[1], vec[0], 0]
        ])
    
    def to_p_and_v(h: Tuple[int, int, int, int, int, int]):
        px, py, pz, vx, vy, vz = h
        return np.array([px, py, pz]), np.array([vx, vy, vz])
    
    p0, v0 = to_p_and_v(hailstones[0])
    p1, v1 = to_p_and_v(hailstones[1])
    p2, v2 = to_p_and_v(hailstones[2])

    matrix = np.ndarray((6, 6))

    print(cross_matrix(v0), cross_matrix(v1))

    matrix[0:3, 0:3] = cross_matrix(v0) - cross_matrix(v1)
    matrix[3:6, 0:3] = cross_matrix(v0) - cross_matrix(v2)
    matrix[0:3, 3:6] = cross_matrix(p1) - cross_matrix(p0)
    matrix[3:6, 3:6] = cross_matrix(p2) - cross_matrix(p0)

   
    rhs = np.ndarray((6))
    rhs[0:3] = -1 * np.cross(p0, v0) + np.cross(p1, v1)
    rhs[3:6] = -1 * np.cross(p0, v0) + np.cross(p2, v2)
    sol = np.linalg.solve(matrix, rhs)
    assert np.allclose(rhs, np.matmul(matrix, sol))
    return sol[0] + sol[1] + sol[2]


if __name__ == "__main__":
    file_name = 'd24-input.text'
    least = 200_000_000_000_000
    most = 400_000_000_000_000
    # file_name = "test_input.text"
    # least = 7
    # most = 24
    hailstones = []

    px, py, pz, vx, vy, vz = [], [], [], [], [], []
    with open(file_name, "r") as f:
        line = f.readline()
        while line:
            pxi, pyi, pzi, vxi, vyi, vzi = parse_line(line.strip())
            px.append(pxi)
            py.append(pyi)
            pz.append(pzi)
            vx.append(vxi)
            vy.append(vyi)
            vz.append(vzi)
            hailstones.append((pxi, pyi, pzi, vxi, vyi, vzi))
            line = f.readline()

    print(part1(hailstones, least, most))
    print(part2(hailstones))

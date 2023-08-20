from PIL import Image


direction_map = ["north", "west", "south", "east"]


def read_pattern(file_path):
    pattern = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            pattern.append(list(line))
    return pattern


def rotate90_matrix(m):
    # rotates a matrix by 90 degrees counter-clockwise
    m2 = []
    for j in range(len(m[0])):
        m2.append([])
        for i in reversed(range(len(m))):
            m2[j].append(m[i][j])
    return m2


def mirror_matrix(m):
    m2 = []
    for i in range(len(m)):
        m2.append([])
        for j in reversed(range(len(m[i]))):
            m2[i].append(m[i][j])
    return m2


def determine_direction(input_matrix, output_matrix):
    current_matrix = input_matrix

    for i in range(4):
        if current_matrix == output_matrix:
            break
        current_matrix = rotate90_matrix(current_matrix)

    if current_matrix != output_matrix: return None

    return direction_map[i], i


def find_cloud_pattern(image_path, pattern):
    image = Image.open(image_path)
    width, height = image.size

    patterns = []
    matches = [[], [], [], []]
    for o in range(4):
        if o != 0: pattern = rotate90_matrix(pattern)
        patterns.append(pattern)
        for y in range(height):
            for x in range(width):
                match = True
                for i in range(len(pattern)):
                    for j in range(len(pattern[i])):
                        pixel_x = (x + j) % width   # wraparound for x-coordinate
                        pixel_y = (y + i) % height  # wraparound for y-coordinate
                        _r, _g, _b, a = image.getpixel((pixel_x, pixel_y))
                        if pattern[i][j] != "?" and (a != 255) == bool(int(pattern[i][j])):
                            match = False
                            break
                    if not match:
                        break
                if match:
                    matches[o].append((x, y))

    return patterns, matches


def get_valid_coords(spawn_range, pixel_z, fast):
    coords = []

    blocks = 8 if fast else 12
    grid_size = blocks * 256

    int_quotient = spawn_range // grid_size
    z_offset = (pixel_z * blocks)

    min_i = -int_quotient - 1
    if (grid_size * min_i) - 4 + z_offset < -spawn_range:
        min_i += 1

    max_i = int_quotient
    if (grid_size * max_i) - 4 + z_offset > spawn_range:
        max_i -= 1

    for i in range(min_i, max_i + 1):
        coords.append(grid_size * i - 4 + z_offset)
    return coords


def main():
    image_path = "clouds.png"
    pattern_path = "pattern.txt"
    from_bottom = False
    fast = False
    spawn_range = 10000

    vertical_direction = ("bottom" if from_bottom else "top").upper()
    print(f"Looking for the pattern from the {vertical_direction}")

    input_pattern = read_pattern(pattern_path)

    if from_bottom:
        input_pattern = mirror_matrix(input_pattern)

    output_patterns, matches = find_cloud_pattern(image_path, input_pattern)
    tot = sum([len(l) for l in matches])
    if tot != 0:
        print(f"Got {tot} match" + ("es" if tot > 1 else "") + "\n")
        for i in range(len(matches)):
            for match in matches[i]:
                input_direction, _direction_index = determine_direction(input_pattern,
                                                     output_patterns[i])
                print(f"the input data was oriented towards {input_direction} and inserted from the " +
                      vertical_direction)
                print("(while the output is always oriented towards north from the TOP)")
                pattern_string = "\n".join(
                    ["".join(p) for p in output_patterns[i]])
                print(f"match at {match} with pattern:" + "\n" + pattern_string)
                valid_z_coords = get_valid_coords(spawn_range, match[1], fast)
                valid_z_coords_string = "\n".join((str(x) for x in valid_z_coords))
                print(f"valid z coords for given spawnrange of {spawn_range} blocks:" + "\n" + valid_z_coords_string
                      + "\n\n")
    else:
        print("Pattern not found")


if __name__ == "__main__":
    main()
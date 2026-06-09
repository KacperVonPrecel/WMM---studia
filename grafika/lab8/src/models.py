import numpy
from moderngl_window.opengl.vao import VAO

def load_quad_2D(program):
    size = 1.0

    positions = []

    positions.append([-size / 2.0, size / 2.0])
    positions.append([-size / 2.0, -size / 2.0])
    positions.append([size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, size / 2.0])
    positions.append([size / 2.0, -size / 2.0])
    positions.append([size / 2.0, size / 2.0])

    positions = numpy.array(positions, dtype=numpy.float32).flatten()

    vao = VAO()
    vao.buffer(positions, "2f", ["in_position"])

    return vao.instance(program)


def load_cube(program):
    size = 1.0

    positions = []
    # Front face
    positions.append([size / 2.0, size / 2.0, size / 2.0])
    positions.append([-size / 2.0, size / 2.0, size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, size / 2.0])
    positions.append([size / 2.0, -size / 2.0, size / 2.0])
    positions.append([size / 2.0, size / 2.0, size / 2.0])
    # Back face
    positions.append([size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, size / 2.0, -size / 2.0])
    positions.append([size / 2.0, size / 2.0, -size / 2.0])
    positions.append([size / 2.0, -size / 2.0, -size / 2.0])
    # Top face
    positions.append([size / 2.0, size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, size / 2.0, size / 2.0])
    positions.append([-size / 2.0, size / 2.0, size / 2.0])
    positions.append([size / 2.0, size / 2.0, size / 2.0])
    positions.append([size / 2.0, size / 2.0, -size / 2.0])
    # Bottom face
    positions.append([size / 2.0, -size / 2.0, size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([size / 2.0, -size / 2.0, size / 2.0])
    # Left face
    positions.append([-size / 2.0, size / 2.0, size / 2.0])
    positions.append([-size / 2.0, size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([-size / 2.0, -size / 2.0, size / 2.0])
    positions.append([-size / 2.0, size / 2.0, size / 2.0])
    # Right face
    positions.append([size / 2.0, size / 2.0, -size / 2.0])
    positions.append([size / 2.0, size / 2.0, size / 2.0])
    positions.append([size / 2.0, -size / 2.0, size / 2.0])
    positions.append([size / 2.0, -size / 2.0, size / 2.0])
    positions.append([size / 2.0, -size / 2.0, -size / 2.0])
    positions.append([size / 2.0, size / 2.0, -size / 2.0])

    normals = []
    # Front face
    normals.append([0.0, 0.0, 1.0])
    normals.append([0.0, 0.0, 1.0])
    normals.append([0.0, 0.0, 1.0])
    normals.append([0.0, 0.0, 1.0])
    normals.append([0.0, 0.0, 1.0])
    normals.append([0.0, 0.0, 1.0])
    # Back face
    normals.append([0.0, 0.0, -1.0])
    normals.append([0.0, 0.0, -1.0])
    normals.append([0.0, 0.0, -1.0])
    normals.append([0.0, 0.0, -1.0])
    normals.append([0.0, 0.0, -1.0])
    normals.append([0.0, 0.0, -1.0])
    # Top face
    normals.append([0.0, 1.0, 0.0])
    normals.append([0.0, 1.0, 0.0])
    normals.append([0.0, 1.0, 0.0])
    normals.append([0.0, 1.0, 0.0])
    normals.append([0.0, 1.0, 0.0])
    normals.append([0.0, 1.0, 0.0])
    # Bottom face
    normals.append([0.0, -1.0, 0.0])
    normals.append([0.0, -1.0, 0.0])
    normals.append([0.0, -1.0, 0.0])
    normals.append([0.0, -1.0, 0.0])
    normals.append([0.0, -1.0, 0.0])
    normals.append([0.0, -1.0, 0.0])
    # Left face
    normals.append([-1.0, 0.0, 0.0])
    normals.append([-1.0, 0.0, 0.0])
    normals.append([-1.0, 0.0, 0.0])
    normals.append([-1.0, 0.0, 0.0])
    normals.append([-1.0, 0.0, 0.0])
    normals.append([-1.0, 0.0, 0.0])
    # Right face
    normals.append([1.0, 0.0, 0.0])
    normals.append([1.0, 0.0, 0.0])
    normals.append([1.0, 0.0, 0.0])
    normals.append([1.0, 0.0, 0.0])
    normals.append([1.0, 0.0, 0.0])
    normals.append([1.0, 0.0, 0.0])

    # Alternative to normals generation
    #generate_normals(positions)

    positions = numpy.array(positions, dtype=numpy.float32).flatten()
    normals = numpy.array(normals, dtype=numpy.float32).flatten()

    vao = VAO()
    vao.buffer(positions, "3f", ["in_position"])
    vao.buffer(normals, "3f", ["in_normal"])
    return vao.instance(program)


def load_pyramid(program, base = 1.0, height = 1.0):

    p0 = [-base / 2.0, -height / 2.0,  base / 2.0]  # front-left
    p1 = [ base / 2.0, -height / 2.0,  base / 2.0]  # front-right
    p2 = [ base / 2.0, -height / 2.0, -base / 2.0]  # back-right
    p3 = [-base / 2.0, -height / 2.0, -base / 2.0]  # back-left
    apex = [0.0, height / 2.0, 0.0]

    positions = []

    # Base, normal down
    positions.append(p0)
    positions.append(p2)
    positions.append(p1)

    positions.append(p0)
    positions.append(p3)
    positions.append(p2)

    # Front side
    positions.append(p0)
    positions.append(p1)
    positions.append(apex)

    # Right side
    positions.append(p1)
    positions.append(p2)
    positions.append(apex)

    # Back side
    positions.append(p2)
    positions.append(p3)
    positions.append(apex)

    # Left side
    positions.append(p3)
    positions.append(p0)
    positions.append(apex)

    normals = generate_normals(positions)

    positions = numpy.array(positions, dtype=numpy.float32).flatten()
    normals = numpy.array(normals, dtype=numpy.float32).flatten()

    vao = VAO()
    vao.buffer(positions, "3f", ["in_position"])
    vao.buffer(normals, "3f", ["in_normal"])
    return vao.instance(program)


def load_sphere(program, radius=0.5, stacks=24, slices=48):
    positions = []
    normals = []

    def sphere_point(i, j):
        theta = numpy.pi * i / stacks
        phi = 2.0 * numpy.pi * j / slices

        x = numpy.sin(theta) * numpy.cos(phi)
        y = numpy.cos(theta)
        z = numpy.sin(theta) * numpy.sin(phi)

        position = [x * radius, y * radius, z * radius]
        normal = [x, y, z]

        return position, normal

    for i in range(stacks):
        for j in range(slices):
            p00, n00 = sphere_point(i, j)
            p01, n01 = sphere_point(i, j + 1)
            p10, n10 = sphere_point(i + 1, j)
            p11, n11 = sphere_point(i + 1, j + 1)

            # Triangle 1
            positions.append(p00)
            positions.append(p01)
            positions.append(p11)

            normals.append(n00)
            normals.append(n01)
            normals.append(n11)

            # Triangle 2
            positions.append(p00)
            positions.append(p11)
            positions.append(p10)

            normals.append(n00)
            normals.append(n11)
            normals.append(n10)

    positions = numpy.array(positions, dtype=numpy.float32).flatten()
    normals = numpy.array(normals, dtype=numpy.float32).flatten()

    vao = VAO()
    vao.buffer(positions, "3f", ["in_position"])
    vao.buffer(normals, "3f", ["in_normal"])
    return vao.instance(program)


def load_torus(program, major_radius=0.5, minor_radius=0.2, major_segments=48, minor_segments=16):
    positions = []
    normals = []

    def torus_point(i, j):
        u = 2.0 * numpy.pi * i / major_segments
        v = 2.0 * numpy.pi * j / minor_segments

        x = (major_radius + minor_radius * numpy.cos(v)) * numpy.cos(u)
        y = minor_radius * numpy.sin(v)
        z = (major_radius + minor_radius * numpy.cos(v)) * numpy.sin(u)

        nx = numpy.cos(v) * numpy.cos(u)
        ny = numpy.sin(v)
        nz = numpy.cos(v) * numpy.sin(u)

        position = [x, y, z]
        normal = [nx, ny, nz]

        return position, normal

    for i in range(major_segments):
        for j in range(minor_segments):
            p00, n00 = torus_point(i, j)
            p01, n01 = torus_point(i, j + 1)
            p10, n10 = torus_point(i + 1, j)
            p11, n11 = torus_point(i + 1, j + 1)

            # Triangle 1
            positions.append(p00)
            positions.append(p01)
            positions.append(p11)

            normals.append(n00)
            normals.append(n01)
            normals.append(n11)

            # Triangle 2
            positions.append(p00)
            positions.append(p11)
            positions.append(p10)

            normals.append(n00)
            normals.append(n11)
            normals.append(n10)

    positions = numpy.array(positions, dtype=numpy.float32).flatten()
    normals = numpy.array(normals, dtype=numpy.float32).flatten()

    vao = VAO()
    vao.buffer(positions, "3f", ["in_position"])
    vao.buffer(normals, "3f", ["in_normal"])
    return vao.instance(program)


def generate_normals(positions):
    N = len(positions)
    normals = []
    for i in range(0, N, 3):
        p0 = numpy.array(positions[i + 0])
        p1 = numpy.array(positions[i + 1])
        p2 = numpy.array(positions[i + 2])
        cross = numpy.cross(p1 - p0, p2 - p0)
        norm = cross / numpy.linalg.norm(cross)
        for v in range(3):
            normals.append(list(norm))
    return normals
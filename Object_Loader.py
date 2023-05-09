class Object:
    def __init__(self, filename, swap_y_z=False):

        # Getting all information about the .obj model
        self.vertices = []
        self.faces = []
        self.normals = []
        self.texture = []
        self.materials = {}
        self.current_material = None

        for line in open(filename, "r"):

            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swap_y_z:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)

            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swap_y_z:
                    v = v[0], v[2], v[1]
                self.normals.append(v)

            elif values[0] == 'vt':
                self.texture.append(list(map(float, values[1:3])))

            elif values[0] == 'f':
                face = []
                texture = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texture.append(int(w[1]))
                    else:
                        texture.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texture))

            elif values[0] == 'usemtl':
                self.current_material = values[1]

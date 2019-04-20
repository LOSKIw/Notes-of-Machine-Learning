import random

dice_faces = {
    1: [1, 1, 1, 1, 0, 1, 1, 1, 1],
    2: [0, 1, 1, 1, 1, 1, 1, 1, 0],
    3: [0, 1, 1, 1, 0, 1, 1, 1, 0],
    4: [0, 1, 0, 1, 1, 1, 0, 1, 0],
    5: [0, 1, 0, 1, 0, 1, 0, 1, 0],
    6: [0, 1, 0, 0, 1, 0, 0, 1, 0]
}

rotations = {   # -1 = White, -2 = Black
    0: [
        [-1, -1, -1, -1, -1],
        [-1,  0,  1,  2, -1],
        [-1,  3,  4,  5, -1],
        [-1,  6,  7,  8, -1],
        [-1, -1, -1, -1, -1]
    ],
    1: [
        [-2, -1,  0, -1, -2],
        [-1,  3, -1,  1, -1],
        [ 6, -1,  4, -1,  2],
        [-1,  7, -1,  5, -1],
        [-2, -1,  8, -1, -2]
    ],
    2: [
        [-1, -1, -1, -1, -1],
        [-1,  6,  3,  0, -1],
        [-1,  7,  4,  1, -1],
        [-1,  8,  5,  2, -1],
        [-1, -1, -1, -1, -1]
    ],
    3: [
        [-2, -1,  6, -1, -2],
        [-1,  7, -1,  3, -1],
        [ 8, -1,  4, -1,  0],
        [-1,  5, -1,  1, -1],
        [-2, -1,  2, -1, -2]
    ]
}

def init_board(v, r, x, y):
    '''初始化数据（全0，矩阵形式）'''
    return {'grid': [[0 for i in range(10)] for j in range(10)], 'seq': None, 'value': v, 'rotation': r, 'x': x, 'y': y}


def generate_sequence(board):
    '''根据生成的信息处理图形并序列化'''
    # 生成骰子图形
    f = dice_faces[board['value']]
    r = rotations[board['rotation']]
    tmp = [[(lambda x, y: f[r[x][y]] if r[x][y] >= 0 else (r[x][y] + 2))(i, j) for j in range(5)] for i in range(5)]
    for y in range(5):
        # 将处理后的骰子复制到版面上
        board['grid'][board['y'] + y][board['x']:board['x'] + 5] = tmp[y][:]
    # 将矩阵形式转换为序列形式
    board['seq'] = [i for j in board['grid'] for i in j]
    return board['seq'], [board['value']/10]


def generate_data(n, gen_rotate=True, random_seed=0):
    '''生成n个数据和结果'''
    x = []
    y = []
    random.seed(random_seed)
    for _ in range(n):
        if gen_rotate:
            b = init_board(random.randint(1, 6), random.randint(0, 3), random.randint(0, 5), random.randint(0, 5))
        else:
            b = init_board(random.randint(1, 6), random.randint(0, 1) * 2, random.randint(0, 5), random.randint(0, 5))
        s, v = generate_sequence(b)
        x.append(s)
        y.append(v)
    return x, y


def generate_all():
    '''生成全部可能的数据和结果'''
    data_x = []
    data_y = []
    for x in range(6):
        for y in range(6):
            for v in [1, 4, 5]:
                for r in [0, 1]:
                    b = init_board(v, r, x, y)
                    generate_sequence(b)
                    data_x.append(b['seq'])
                    data_y.append([b['value'] / 10])
            for v in [2, 3, 6]:
                for r in [0, 1, 2, 3]:
                    b = init_board(v, r, x, y)
                    generate_sequence(b)
                    data_x.append(b['seq'])
                    data_y.append([b['value'] / 10])
    return data_x, data_y



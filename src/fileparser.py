def parseFile(filepath):
    board = []

    with open(filepath, 'r') as f:
        lines = f.readlines()
        f.close()
    
    for line in lines:
        nodes = line.split()
        nodes[len(nodes)-1] = nodes[len(nodes)-1].replace('\n', '')
        for i in range(0, len(nodes)):  # Convert numeric cells into ints
            item = nodes[i]
            if item.isnumeric():
                nodes[i] = int(item)

        board.append(nodes)

    return board

'''

    Basic information
You have been given a chess board of size 8x8 and a chess piece Horse.

    Task explanation

1) To come up with and write down an algorithm for traversing all cells of a chessboard by
stepping on each cell 1 time.
2) Visually show the numbering of moves on the board.

    Conditions

The starting position of the horse must be dynamic. (you can start from any cell)

'''

def knight(x0, y0, done, size=8):
    desc = [[0 for j in range(size)] for i in range(size)]
    desc[x0][y0] = 1
    
    dx = [2, 1, -1, -2, -2, -1, 1, 2]
    dy = [1, 2, 2, 1, -1, -2, -2, -1]

    def can_be_done(u, v, i):
        desc[u][v] = i
        done = try_next(u, v, i)
        if not done:
            desc[u][v] = 0
        return done
    def try_next(x,y, i):
        
        env = {'done': False, 'eos': False, 'u': x, 'v': y, 'k': -1}

        def next():
            x = env['u']
            y = env['v']
            while env['k'] < 8:
                env['k'] +=1
                if env['k'] < 8:
                    env['u'] = x + dx[env['k']]
                    env['v'] = y + dy[env['k']]
                if (env['u'] >= 0 and env['u']<size) and (env['v']>=0 and env['v']<size) and desc[env['u']][env['v']]==0:
                    break
            env['eos'] = (env['k']==8)

        if i < size**2:
            next()
            while not env['eos'] and not can_be_done(env['u'], env['v'], i+1):
                next()
            done = not env['eos']
        else:
            done = True
        return done

    try_next(x0, y0, 1)
    for i in desc:
        for j in i:
            print(j, end=' ')
        print('\t')

knight(0, 0, False)
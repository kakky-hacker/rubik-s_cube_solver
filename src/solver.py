import chainer
import chainer.functions as F
import chainer.links as L
import chainerrl
import pickle
from random import randint, choice
import numpy as np
from copy import deepcopy

def benchmark(n = 100):
    clear, time = 0, 0
    solver = Solver()
    for _ in range(n):
        #問題作成
        problem = _Cube().random()
        #解く
        ans = solver.solve(problem)
        if  ans != []:
            clear += 1
            time += len(ans)
    return (clear/n)*100, time/clear
    
class Solver:
    def __init__(self):
        #Agent設定
        q_func = QFunction()
        optimizer = chainer.optimizers.Adam(alpha=5e-6, eps=1e-4)
        optimizer.setup(q_func)
        gamma = 0.99
        explorer = chainerrl.explorers.LinearDecayEpsilonGreedy(start_epsilon=0., end_epsilon=0.,
                                                            decay_steps=10000, random_action_func=lambda:randint(0, 5))
        replay_buffer = chainerrl.replay_buffer.PrioritizedReplayBuffer(capacity=10**6)
        phi = lambda x: x.astype(np.float32, copy=False)
        self.agent = chainerrl.agents.DoubleDQN(q_func, optimizer, replay_buffer, gamma, explorer,
                                 replay_start_size=1000000, minibatch_size=512, update_interval=16,
                                 target_update_interval=200, phi=phi)
        self.agent.load("Agent")
        #キューブ設定
        self.cube = _Cube()
        #解を保持
        self.answer = []

    def solve(self, problem):
        ans = self._solve(problem)
        if ans == None:
            ans = [-1] * 100
        elif len(ans) < 15:
            return ans
        env = [_Cube() for _ in range(36)]
        i = 0
        for cube in env:
            cube.set(problem)
            act1 = cube.rotate(i//6)
            act2 = cube.rotate(i%6)
            i += 1
            _ans = self._solve(deepcopy(cube.masu))
            if _ans != None and len(_ans) < len(ans):
                _ans.insert(0, act1)
                _ans.insert(1, act2)
                ans = deepcopy(_ans)
                if len(ans) < 12:
                    break
        if ans == [-1] * 100:
            return []
        return ans

    def _solve(self, problem):
        self.answer = []
        self.cube.set(problem)
        flag = False
        for _ in range(30):
            if self.cube.complete():
                flag = True
                break
            self.answer.append(self.cube.rotate(self.agent.act(self.cube.observe())))
        if flag:
            res = []
            for ans in self.answer:
                if len(res) >= 2 and ans == res[-1] and ans == res[-2]:
                    ans = (ans[0], 1 - ans[1])
                    res.pop(-1)
                    res.pop(-1)
                    res.append(ans)
                    continue
                res.append(ans)
            return res
        return None

class QFunction(chainer.Chain):
    def __init__(self):
        w = chainer.initializers.HeNormal(scale=1.0)
        Ln = 1250
        super(QFunction, self).__init__()
        with self.init_scope():
            self.l1 = L.Linear(84, Ln, initialW=w)
            self.s1 = L.Swish(Ln)
            self.l2 = L.Linear(Ln, Ln, initialW=w)
            self.s2 = L.Swish(Ln)
            self.l3 = L.Linear(Ln, Ln, initialW=w)
            self.s3 = L.Swish(Ln)
            self.l4 = L.Linear(Ln, Ln, initialW=w)
            self.s4 = L.Swish(Ln)
            self.l5 = L.Linear(Ln, Ln, initialW=w)
            self.s5 = L.Swish(Ln)
            self.l6 = L.Linear(Ln, Ln, initialW=w)
            self.s6 = L.Swish(Ln)
            self.l7 = L.Linear(Ln, Ln, initialW=w)
            self.s7 = L.Swish(Ln)
            self.l8 = L.Linear(Ln, Ln, initialW=w)
            self.s8 = L.Swish(Ln)
            self.l9 = L.Linear(Ln, 6, initialW=w)

    def __call__(self, x):
        h = self.s1(self.l1(x))
        h = self.s2(self.l2(h))
        h = self.s3(self.l3(h))
        h = self.s4(self.l4(h))
        h = self.s5(self.l5(h))
        h = self.s6(self.l6(h))
        h = self.s7(self.l7(h))
        h = self.s8(self.l8(h))
        return chainerrl.action_value.DiscreteActionValue(self.l9(h))

class _Cube:
    
    red = 0
    green = 1
    orange = 2
    blue = 3
    yellow = 4
    white = 5
    xf = 0
    xb = 1
    yf = 2
    yb = 3
    zf = 4
    zb = 5
    left = 0
    right = 1

    def __init__(self):
        self.masu = np.array([self.red]*4 + [self.green]*4 + [self.orange]*4
                             + [self.blue]*4 + [self.yellow]*4 + [self.white]*4)
        self.before_action = [-1]*3

    def set(self, problem):
        self.masu = np.array(problem).flatten()
        self.before_action = [-1]*3

    def observe(self):
        obs = [0] * 84
        i = 0
        for color in self.masu[:15]:
            if i != 2:
                j = i if i < 2 else i - 1
                obs[color*14 + j] = 1
            i += 1
        return np.array(obs).astype(np.float32)

    def complete(self):
        for i, j in zip(self.masu[:16], np.array([self.red]*4 + [self.green]*4 + [self.orange]*4 + [self.blue]*4)):
            if i != j:
                return False
        return True

    def random(self, n=50):
        for _ in range(n):
            action = randint(0, 5)
            self.rotate(action)
        return self.masu

    def rotate(self, action):
        menn, muki = (action//2)*2+1, action % 2
        #千日手から脱却
        if self.before_action[-1] == menn + (1 - muki):
            for _ in range(10):
                menn, muki = choice([1, 3, 5]), randint(0, 1)
                if self.before_action[-1] != menn + (1 - muki):
                    break
        elif all([x == menn + muki for x in self.before_action]):
            for _ in range(10):
                menn, muki = choice([1, 3, 5]), randint(0, 1)
                if all([x == menn + muki for x in self.before_action]):
                    break
        self.before_action.pop(0)
        self.before_action.append(menn + muki)
        #回転
        _masu = self.masu
        if menn == self.xb:
            if muki == self.right:
                _masu[16:20] = _masu[18], _masu[16], _masu[19], _masu[17]
                _masu[0], _masu[1], _masu[4], _masu[5], _masu[8], _masu[9], _masu[12], _masu[13] = _masu[4], _masu[5], _masu[8], _masu[9], _masu[12], _masu[13], _masu[0], _masu[1]
            else:
                _masu[16:20] = _masu[17], _masu[19], _masu[16], _masu[18]
                _masu[0], _masu[1], _masu[4], _masu[5], _masu[8], _masu[9], _masu[12], _masu[13] = _masu[12], _masu[13], _masu[0], _masu[1], _masu[4], _masu[5], _masu[8], _masu[9]
        elif menn == self.yb:
            if muki == self.right:
                _masu[8:12] = _masu[10], _masu[8], _masu[11], _masu[9]
                _masu[5], _masu[7], _masu[22], _masu[20], _masu[14], _masu[12], _masu[18], _masu[16] = _masu[22], _masu[20], _masu[14], _masu[12], _masu[18], _masu[16], _masu[5], _masu[7]
            else:
                _masu[8:12] = _masu[9], _masu[11], _masu[8], _masu[10]
                _masu[5], _masu[7], _masu[22], _masu[20], _masu[14], _masu[12], _masu[18], _masu[16] = _masu[18], _masu[16], _masu[5], _masu[7], _masu[22], _masu[20], _masu[14], _masu[12]
        elif menn == self.zb:
            if muki == self.right:
                _masu[4:8] = _masu[6], _masu[4], _masu[7], _masu[5]
                _masu[22], _masu[23], _masu[3], _masu[1], _masu[17], _masu[16], _masu[8], _masu[10] = _masu[8], _masu[10], _masu[22], _masu[23], _masu[3], _masu[1], _masu[17], _masu[16]
            else:
                _masu[4:8] = _masu[5], _masu[7], _masu[4], _masu[6]
                _masu[22], _masu[23], _masu[3], _masu[1], _masu[17], _masu[16], _masu[8], _masu[10] = _masu[3], _masu[1], _masu[17], _masu[16], _masu[8], _masu[10], _masu[22], _masu[23]
        else:
            print("command error:", action)
        return [menn, muki]

#print(benchmark(n=100))

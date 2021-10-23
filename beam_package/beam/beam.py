from beam_package.utils.sign_convention import DIRECTION
from beam_package.loads.common_loads import Moment, PointLoad, Udl, Uvl
from beam_package.utils.dataholder import LoadTable
from beam_package.singularity.exponents import SINGULARITY_EXPONENT
from beam_package.loads.loadbase import LoadBase
import numpy as np
import matplotlib.pyplot as plt
import json

class Beam:
    def __init__(self, length=None, segments=1000, json_path=None):
        if json_path:
            with open(json_path) as f:
                self.json_obj = json.load(f)
            self.length = self.json_obj['length']
        else:
            self.length = length
        self.segments = segments
        self.x = np.linspace(start=0, stop=self.length, num=self.segments, dtype=np.float64)
        self.load_table = LoadTable()
        self.reactions = None
        self.sfd_matrix = np.zeros(shape=(self.segments,),dtype=np.float64)
        self.bmd_matrix = np.zeros(shape=(self.segments,))

    def add_load(self, load_obj: LoadBase, inplace=True):
        self.sfd_matrix += load_obj.get_singular_sfd_matrix(self.x)
        self.bmd_matrix += load_obj.get_singular_bmd_matrix(self.x)
        output = self.load_table.append(load_obj.load_table, ignore_index=True)
        if inplace:
            self.load_table = output
            # self.load_table.set_index(keys=['Id'], inplace=True)
        return output

    def add_support(self, pos: float, kind='pin'):
        if kind in ['pin', 'roller', 'fixed']:
            vertical_unknown = PointLoad(np.NAN, DIRECTION.UP, pos)
            vertical_unknown.idx_tuple = ('RP',  vertical_unknown.IDX)
            self.add_load(vertical_unknown)
        if kind == 'fixed':
            moment_unknown = Moment(np.NAN, DIRECTION.CW, pos)
            moment_unknown.idx_tuple = ('RM', moment_unknown.IDX)
            self.add_load(moment_unknown)


    def calc_reaction(self, upadate=True):
        '''
        logic:
         x = (A^-1) . B
         where, x is the reaction matrix 2x1
         A is the matrix of co-efficients 2x2
         B is the matric of constants 2x1
        '''
        temp_load_table = (self.load_table.iloc[:, 1:]).copy()
        knowns = temp_load_table.dropna()
        unknowns = temp_load_table[temp_load_table['load'].isna()]
        
        constant_matrix = np.array([
            [knowns[knowns['exponent'] != SINGULARITY_EXPONENT.MOMENT]['point_load'].sum()], # sum of point loads
            [knowns['moment'].sum()]  # sum of moments
        ], dtype=np.float64)
        coefficient_matrix = np.array([
            [1,1],
            unknowns['moment_arm']
        ], dtype=np.float64)

        solution = np.dot(
            np.linalg.inv(coefficient_matrix),
            constant_matrix
        )
        sign_adjustment_matrix = np.array([
            [-1],
            [-1]
        ])
        solution = solution * sign_adjustment_matrix
        self.reactions = solution
        if not upadate:
            print('Solved Reactions: ',self.reactions)
        elif upadate:
            self._update_reactions()

    def _update_reactions(self):
        keep = {'Id': 0,'exponent': 1,'pos0': 2}
        temp_load_table = self.load_table
        unknowns = temp_load_table[temp_load_table['load'].isna()][keep.keys()]
        for serial, load in unknowns.iterrows():
            load_value = self.reactions.flatten()[serial]
            print(load_value)
            if 'RP' in load['Id']:
                direction = DIRECTION.UP if load_value>0 else DIRECTION.DOWN
                p = PointLoad(load_value*direction, direction, load['pos0'])
                self.sfd_matrix += p.get_singular_sfd_matrix(self.x)
                self.bmd_matrix += p.get_singular_bmd_matrix(self.x)
                p.idx_tuple = ('RP', p.IDX)
                self.load_table = self.load_table[self.load_table['Id'] != load['Id']]
                self.add_load(p)
            elif 'RM' in load['Id']:
                direction = DIRECTION.CW if load_value > 0 else direction.ACW
                m = Moment(load_value*direction, direction, load['pos0'])
                self.sfd_matrix += m.get_singular_sfd_matrix(self.x)
                self.bmd_matrix += m.get_singular_bmd_matrix(self.x)
                m.idx_tuple = ('RM', m.IDX)
                self.load_table = self.load_table[self.load_table['Id'] != load['Id']]
                self.add_load(m)

    def evaluate_json(self):
        def get_load_obj(d):
            type_ = d['type']
            sign_ = {
                'down': DIRECTION.DOWN,
                'up': DIRECTION.UP,
                'acw': DIRECTION.ACW,
                'cw': DIRECTION.CW
            }
            if type_ == 'p':
                out = PointLoad(d['magnitude'], sign_[d['direction']], d['position'])
            elif type_ == 'm':
                out = Moment(d['magnitude'], sign_[d['direction']], d['position'])
            elif type_ == 'udl':
                out = Udl(d['magnitude'], sign_[d['direction']], d['start'], d['end'])
            elif type_ == 'uvl':
                out = Uvl(d['magnitude'], sign_[d['direction']], d['posZero'], d['posPeak'])
            return out
        # add supports
        for support in self.json_obj['supports']:
            self.add_support(support['position'], kind=support['type'])
        
        # add loads
        for load in self.json_obj['loads']:
            self.add_load(get_load_obj(load))

    def draw(self):
        fig, (sfd, bmd) = plt.subplots(nrows=2, ncols=1)
        sfd.plot(self.x, self.sfd_matrix)
        sfd.plot(self.x, self.bmd_matrix)
        sfd.set_title('SFD')
        bmd.set_title('BMD')
        sfd.spines['bottom'].set_position('zero')
        sfd.spines['left'].set_position('zero')
        sfd.spines['right'].set_color('none')
        sfd.spines['top'].set_color('none')
        sfd.set_xlim(0, self.length+5)
        bmd.set_xlim(0, self.length + 5)
        bmd.spines['bottom'].set_position('zero')
        bmd.spines['left'].set_position('zero')
        bmd.spines['right'].set_color('none')
        bmd.spines['top'].set_color('none')
        print(self.sfd_matrix)
        # plt.show()
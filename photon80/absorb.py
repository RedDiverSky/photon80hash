#AES-Permutation algorithm 
from collections import deque
import numpy as np

fieldmult2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
              [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
              [0, 3, 6, 5, 12, 15, 10, 9, 11, 8, 13, 14, 7, 4, 1, 2],
              [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
              [0, 5, 10, 15, 7, 2, 13, 8, 14, 11, 4, 1, 9, 12, 3, 6],
              [0, 6, 12, 10, 11, 13, 7, 1, 5, 3, 9, 15, 14, 8, 2, 4],
              [0, 7, 14, 9, 15, 8, 1, 6, 13, 10, 3, 4, 2, 5, 12, 11],
              [0, 8, 3, 11, 6, 14, 5, 13, 12, 4, 15, 7, 10, 2, 9, 1],
              [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
              [0, 10, 7, 13, 14, 4, 9, 3, 15, 5, 8, 2, 1, 11, 6, 12],
              [0, 11, 5, 14, 10, 1, 15, 4, 7, 12, 2, 9, 13, 6, 8, 3],
              [0, 12, 11, 7, 5, 9, 14, 2, 10, 6, 1, 13, 15, 3, 4, 8],
              [0, 13, 9, 4, 1, 12, 8, 5, 2, 15, 11, 6, 3, 14, 10, 7],
              [0, 14, 15, 1, 13, 3, 2, 12, 9, 7, 6, 8, 4, 10, 11, 5],
              [0, 15, 13, 2, 9, 6, 4, 11, 1, 14, 12, 3, 8, 7, 5, 10]]

class permutation:
    
    def __init__(self, input_hash,round_num=12):
        
        self.input = input_hash
        self.input_len = len(input_hash)
        self.round_num = round_num
        self.each_round_value = []
    
    def rc(self,v):
        if v == 1:
            return [1, 0, 2, 7, 5]
        elif v == 2:
            return [3, 2, 0, 5, 7]
        elif v == 3:
            return [7, 6, 4, 1, 3]
        elif v == 4:
            return [14, 15, 13, 8, 10]
        elif v == 5:
            return [13, 12, 14, 11, 9]
        elif v == 6:
            return [11, 10, 8, 13, 15]
        elif v == 7:
            return [6, 7, 5, 0, 2]
        elif v == 8:
            return [12, 13, 15, 10, 8]
        elif v == 9:
            return [9, 8, 10, 15, 13]
        elif v == 10:
            return [2, 3, 1, 4, 6]
        elif v == 11:
            return [5, 4, 6, 3, 1]
        elif v == 12:
            return [10, 11, 9, 12, 14]
    
    def shift_row(self):
        
        result_shiftrow = []
        for row in range(self.input_len):
            item = deque(self.input[row])
            item.rotate(-row)
            result_shiftrow.append(list(item))
        
        self.input = result_shiftrow
        
        return result_shiftrow
        
    def subcell(self):

        sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
        result_subcell = self.input
        for i in range(0, self.input_len):
            for j in range(0, self.input_len):
                result_subcell[i][j] = sbox[int(self.input[i][j])]
        
        self.input = result_subcell
        
        return result_subcell
                
    def addconstant(self,v):
   
        result_addconstant = self.input

        for i in range(0, self.input_len):
            result_addconstant[i][0] = self.input[i][0] ^ self.rc(v)[i]
        
        self.input = result_addconstant
        
        return result_addconstant
        
    
    def mixcolumn(self):

        A_t = [[1, 2, 9, 9, 2],
               [2, 5, 3, 8, 13],
               [13, 11, 10, 12, 1],
               [1, 15, 2, 3, 14],
               [14, 14, 8, 5, 12]]

        #irreducible polynomial  = x^4+x+1 : 10011

        result_mixcolumn = [[0 for x in range(self.input_len)] for x in range(self.input_len)]
        xor_sum = 0
        for i in range(0, self.input_len):
            for j in range(0, self.input_len):
                for k in range(0, self.input_len):
                    xor_sum = xor_sum ^ fieldmult2[A_t[i][k]][self.input[k][j]]
                result_mixcolumn[i][j] = xor_sum
                xor_sum = 0
        
        self.input = result_mixcolumn
        
        return result_mixcolumn
    
    def get_each_round(self):
        
        return self.each_round_value
               
            
    def permutation_result(self):
        
        for i in range(self.round_num):
            
            self.addconstant(i+1)
            self.subcell()
            self.shift_row()
            self.mixcolumn()
            self.each_round_value.append(self.input)
            
        return self.input
    


class absorb:
    
    def __init__(self,input_hash):
        
        self.State= [[0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,0],
                     [0,0,0,0,1],
                     [4,1,4,1,0]] 
        
        self.input_hash = input_hash
        self.input_len = len(input_hash)
        
        
    def xor_message(self):
        
        current_state = np.array(self.State[0])
        message = np.array(self.input_hash[0])
        self.State[0] = list(current_state^message)
        self.input_hash.pop(0)
        
    def result_absorb(self):
        
        for message in range(self.input_len):
            
            self.xor_message()
            #print("Message {}".format(self.State[0]))
            permutation_ = permutation(self.State)
            self.State = permutation_.permutation_result()
            #print("Permutation {} \n:".format(message))
            #print(self.State)
            #print("---------------------------------")
            
        return self.State
            
               
            
    
    
    
       

        
        

            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
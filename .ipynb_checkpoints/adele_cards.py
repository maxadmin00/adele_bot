import random 

class Console:
    def __init__(self):
        self.caps = {'green': [],
                    'gray': [],
                    'red': [],
                    'purple': [],
                    'black': [],
                    'blue': []}
        
        self.possible_caps = {'green': 9,
                              'gray': 9,
                              'red': 9,
                              'purple': 9,
                              'black': 9,
                              'blue': 9
                            }
        self.anomalies = [random.choice(['закрыть люки', 'деактивированные терминалы',
                                         'разряженные батареи', 'взрывы', 'паника', 'атака'])
                                         for _ in range(4)]
    
    def add_cap(self):
        cap = random.choice(list(self.possible_caps.keys()))
        if self.possible_caps[cap] == 1:
            self.possible_caps.pop(cap)
        else:
            self.possible_caps[cap] -= 1
        
        add = None
        amount = self.caps[cap]
        if cap == 'green':
            if amount <= 3:
                add = 2
            elif amount <= 5:
                add = 3
            elif amount <=6:
                add 
        self.caps[cap]
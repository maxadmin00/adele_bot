import random 
import numpy as np

class Console:
    def __init__(self):
        self.move_number = 1
        self.energy = 15
        self.caps = {'шпионаж': [],
                    'заблокированная дверь': [],
                    'пожар': [],
                    'гипоксия': [],
                    'тьма': [],
                    'блокировка': []}
        self.played_caps = 0
        
        self.possible_caps = {'шпионаж': 9,
                              'заблокированная дверь': 9,
                              'пожар': 9,
                              'гипоксия': 9,
                              'тьма': 9,
                              'блокировка': 9
                            }
        self.anomalies = [random.choice(['закрыть люки', 'деактивированные терминалы',
                                         'разряженные батареи', 'взрывы', 'паника', 'атака'])
                                         for _ in range(4)]
        self.deck = ['любая'] * 3
        possible_rooms = [str(i) for i in range(1, 21)]
        for i in range(24):
            r1 = random.choice(possible_rooms)
            r2 = random.choice(possible_rooms)
            while r1 == r2:
                r2 = random.choice(possible_rooms)

            comb = r1 + ' или ' + r2
            self.deck.append(comb)
        
        self.cards = []
        for i in range(4):
            self.draw_card()
            self.draw_cap()

    def new_move(self):
        self.move_number += 1
        self.energy += 10

    def get_console_info(self):
        return f'''доступно энергии {self.energy}
                доступно аномалий {len(self.anomalies)}. стоимость одной аномалии: 5 единиц энергии
                карты на руках (отображают возможное расположение фишек): {', '.join(self.cards)}
                доступные фишки опасности: {', '.join([key + ' ' + str(len(value)) + ' штук' for key, value in self.caps.items()])}
                '''
    
    def draw_card(self):
        card_ind = random.randint(0, len(self.deck) - 1)
        self.cards.append(self.deck[card_ind])
        self.deck.pop(card_ind)
    
    def draw_cap(self):
        cap = random.choice(list(self.possible_caps.keys()))
        if self.possible_caps[cap] == 1:
            self.possible_caps.pop(cap)
        else:
            self.possible_caps[cap] -= 1
        
        add = None
        if len(self.caps[cap]) == 0:
            add = 2
        else:
            add = np.floor(np.log2(len(self.caps[cap]) + 1))
        self.caps[cap].append(add)

    def play_anomaly(self, anomaly_ind: int = 1):
        """anomaly_ind: int - порядковый номер карты аномалии которую выбрали к розыгрышу"""
        if self.played_caps > 3 and self.energy > 5:
            anomaly = self.anomalies[anomaly_ind]
            self.anomalies.pop(anomaly_ind)
            self.played_caps -= 3
            self.energy -= 5
            return f'разыграна аномалия {anomaly}'
        elif self.energy < 5:
            return 'не хватает энергии'
        else:
            return 'сыграно слишком мало фишек'

    def play_card(self, room: int = 1, cap: str = 'шпионаж'):
        """room: str - номер комнаты в которую нужно сыграть фишку
        cap: str - фишка которую надо сыграть"""
        has_room = False
        card = None
        for i, comb in enumerate(self.cards):
            if room in comb:
                has_room = True
                card = i
                break
        
        for i, comb in enumerate(self.cards):
            if 'любая' == comb:
                has_room = True
                card = i
        
        if not has_room:
            return 'нужной карты комнаты нет'
        
        if len(self.caps[cap]) == 0:
            return 'нужной фишки нет'
        
        if self.energy < self.caps[cap][-1]:
            return 'не хватает энергии' 
        
        self.energy -= self.caps[cap].pop()
        self.cards.pop(card)
        self.draw_cap()
        self.draw_cap()
        return f'разыграна фишка {cap} в комнату {room}'

        
    
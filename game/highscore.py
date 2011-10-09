import pickle
import random

#Handle highscores
class Highscores_data():
    def __init__(self):
        self.names = ['James', 'John', 'George', 'Anne', 'Albert', 'Zack', 'Michelle', 'Fionna']
        self.surnames = ['Appleton', 'Lennon', 'Potter', 'Stevenson', 'Dawkins', 'Zemeckis', 'Ford', 'Johnson']
        self.num_highscores = 5
        try:
            self.values = pickle.load(open('highscores.p', 'rb'))
        except:
            print "Highscores file not available, creating new one"
            self.values = []
            for i in range(0,self.num_highscores):
                #Choose a random name
                name        = self.names[random.randint(0,len(self.names)-1)]
                surname    = self.surnames[random.randint(0,len(self.surnames)-1)]
                self.values.append({'name': "{0} {1}".format(name, surname), 'score':(10000-i*500)+random.randint(-300, 300)})
            pickle.dump(self.values, open('highscores.p', 'wb'))

    def get_highscores(self):
        return self.values
                    
    def set_newhighscore(self, name, score):
        i = 0
        for highscores in self.values:
            if score> highscores['score']:
                self.values.insert(i, {'name':name,'score':score})
                break
            i += 1
        if (len(self.values) > self.num_highscores):
            self.values = self.values[0:self.num_highscores]
            pickle.dump(self.values, open('highscores.p', 'wb'))

    def print_highscores(self):
        for score in self.values:
            print "{0}: {1}\n".format(score['name'], score['score'])




class Calculation:

    def formule(self, cas_favorable, cas_possible):
        probability_of = (cas_favorable / cas_possible) * 100
        probability_of = round(probability_of, 2)
        
        return probability_of

    def probability_calculation(self, perplexity):
        tab_ai = []
        tab_humain = []
        for per in perplexity:
            if per < self.critical_level_ai.get():
                tab_ai.append(1)
            else:
                tab_humain.append(1)
        cas_possible = sum(tab_humain) + sum(tab_ai)
        
        probability_ai = self.formule(sum(tab_ai), cas_possible)
        probability_huamin = self.formule(sum(tab_humain), cas_possible)
        
        return (probability_ai, probability_huamin)

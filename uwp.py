import dice

class Element:
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def __init__(self):
        self.hex = self.generate()

    def generate(self):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6) - 2
        return self.__class__.hexes[roll]

    def getHex(self):
        return self.hex

    def get_value(self):
        return self.__class__.hexes.index(self.hex)

    def set(self, hex):
        if hex in self.__class__.hexes:
            self.hex = hex

class Starport(Element):
    hexes = ['A', 'B', 'C', 'D', 'E', 'X']

    def __init__(self, settlement="Standard"):
        self.hex = self.generate(settlement)

    def generate(self, settlement):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if settlement == "Backwater":
            return self.generateBackwater(roll)
        elif settlement == "Mature":
            return self.generateMature(roll)
        elif settlement == "Cluster":
            return self.generateCluster(roll)
        else:
            return self.generateStandard(roll)

    def generateStandard(self, roll):
        if roll >=2 and roll <= 4:
            hex = 'A'
        elif roll >= 5 and roll <= 6:
            hex = 'B'
        elif roll >= 7 and roll <= 8:
            hex = 'C'
        elif roll == 9:
            hex = 'D'
        elif roll >= 10 and roll <= 11:
            hex = 'E'
        else:
            hex = 'X'
        return hex

    def generateBackwater(self, roll):
        if roll >=2 and roll <= 3:
            hex = 'A'
        elif roll >= 4 and roll <= 5:
            hex = 'B'
        elif roll >= 7 and roll <= 8:
            hex = 'C'
        elif roll == 9:
            hex = 'D'
        elif roll >= 10 and roll <= 11:
            hex = 'E'
        else:
            hex = 'X'
        return hex

    def generateMature(self, roll):
        if roll >=2 and roll <= 4:
            hex = 'A'
        elif roll >= 5 and roll <= 6:
            hex = 'B'
        elif roll >= 7 and roll <= 8:
            hex = 'C'
        elif roll == 9:
            hex = 'D'
        else:
            hex = 'E'
        return hex

    def generateCluster(self, roll):
        if roll >=2 and roll <= 5:
            hex = 'A'
        elif roll >= 6 and roll <= 7:
            hex = 'B'
        elif roll >= 8 and roll <= 9:
            hex = 'C'
        elif roll == 10:
            hex = 'D'
        elif roll == 11:
            hex = 'E'
        else:
            hex = 'X'
        return hex

class Size(Element):
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']

class Atmosphere(Element):
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
    
    def __init__(self, size):
        self.hex = self.generate(size)

    def generate(self, size):
        if size.getHex() == '0':
            return '0'
        dm = size.get_value()
        mydice = dice.Dice()
        roll = mydice.roll(2, 6) - 7 + dm
        if roll >= len(self.__class__.hexes):
            return self.__class__.hexes[-1]
        if roll < 0:
            return '0'
        return self.__class__.hexes[roll]

class Hydrosphere(Element):
     hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']

     def __init__(self, size, atmosphere):
         self.hex = self.generate(size, atmosphere)

     def generate(self, size, atmosphere):
         if size.getHex() == '0':
            return '0'
         dm = atmosphere.get_value()
         if atmosphere.getHex() <= '1' and atmosphere.getHex() >= 'A':
            dm -= 4
         mydice = dice.Dice()
         roll = mydice.roll(2, 6) - 7 + dm
         if roll >= len(self.__class__.hexes):
             return self.__class__.hexes[-1]
         if roll < 0:
             return '0'
         return self.__class__.hexes[roll]

class Population(Element):
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A']

class Government(Element):
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D']

    def __init__(self, population):
        self.hex = self.generate(population)

    def generate(self, population):
        dm = population.get_value()
        mydice = dice.Dice()
        roll = mydice.roll(2, 6) - 7 + dm
        if roll >= len(self.__class__.hexes):
            return self.__class__.hexes[-1]
        if roll < 0:
            return '0'
        return self.__class__.hexes[roll]
           
class Law(Element):
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, government):
        self.hex = self.generate(government)

    def generate(self, government):
        dm = government.get_value()
        mydice = dice.Dice()
        roll = mydice.roll(2, 6) - 7 + dm
        if roll >= len(self.__class__.hexes):
            return self.__class__.hexes[-1]
        if roll < 0:
            return '0'
        return self.__class__.hexes[roll]

class Tech(Element):
    def __init__(self, starport, size, atmosphere, hydrosphere, population, government):
        self.hex = self.generate(starport, size, atmosphere, hydrosphere, population, government)

    def generate(self, starport, size, atmosphere, hydrosphere, population, government):
        dm = 0
        if starport.getHex() == 'A':
            dm += 6
        elif starport.getHex() == 'B':
            dm += 4
        elif starport.getHex() == 'C':
            dm += 2
        elif starport.getHex() == 'X':
            dm += -4

        if size.getHex() <= '1':
            dm += 2
        elif size.getHex() <= '4':
            dm += 1

        if atmosphere.getHex() <= '3' or atmosphere.getHex() >= 'A':
            dm += 1

        if hydrosphere.getHex() == '9':
            dm += 1
        elif hydrosphere.getHex() == 'A':
            dm += 2

        if population.getHex() >= '1' and population.getHex() <= '5':
            dm += 1
        elif population.getHex() == '9':
            dm += 2
        elif population.getHex() == 'A':
            dm += 4

        if government.getHex() == '0' or government.getHex() == '5':
            dm += 1
        elif government.getHex() == 'D':
            dm += -2

        mydice = dice.Dice()
        roll = mydice.roll(1, 6) + dm
        if roll < 0:
            return '0'
        return self.__class__.hexes[roll]

class Base(Element):
    """ TODO: Non imperial bases """
    hexes = [' ', 'N', 'S', 'A']
    def __init__(self, starport):
        self.hex = self.generate(starport)

    def generate(self, starport):
        naval = self.getNaval(starport)
        scout = self.getScout(starport)
        if naval and scout:
            return 'A'
        elif naval:
            return 'N'
        elif scout:
            return 'S'
        else:
            return ' '

    def getNaval(self, starport):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if starport.getHex() == 'A':
            if roll >= 8:
                return True
        elif starport.getHex() == 'B':
            if roll >= 8:
                return True
        return False

    def getScout(self, starport):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if starport.getHex() == 'A':
            if roll >= 10:
                return True
        elif starport.getHex() == 'B':
            if roll >= 9:
                return True
        elif starport.getHex() == 'C':
            if roll >= 8:
                return True
        elif starport.getHex() == 'D':
            if roll >= 7:
                return True
        return False

class Zone(Element):
    hexes = [' ', 'A', 'R']

    def __init__(self, starport, government, law):
        self.hex = self.generate(starport, government, law)

    def generate(self, starport, government, law):
        if self.getRed(starport, government, law):
            return 'R'
        elif self.getAmber(government, law):
            return 'A'
        else:
            return ' '
    
    def getAmber(self, government, law):
        govhex = government.getHex()
        lawhex = law.getHex()
        if govhex == 'A' and lawhex >= 'L':
            return True
        elif govhex == 'B' and lawhex >= 'K':
            return True
        elif govhex == 'C' and lawhex >= 'J':
            return True
        elif govhex == 'D' and lawhex >= 'H':
            return True
        elif govhex == 'E' and lawhex >= 'H':
            return True
        elif govhex >= 'F' and lawhex >= 'G':
            return True
        else:
            return False

    def getRed(self, starport, government, law):
        govhex = government.getHex()
        lawhex = law.getHex()
        if starport.getHex() == 'X':
            return True
        if govhex == 'D' and lawhex >= 'L':
            return True
        elif govhex == 'E' and lawhex >= 'K':
            return True
        elif govhex >= 'F' and lawhex >= 'J':
            return True
        else:
            return False

class PopulationMultiplier(Element):
    hexes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    def generate(self):
        mydice = dice.Dice()
        roll = dice.roll(1, 10)
        return self.__class__.hexes[roll - 1]

class GasGiants(Element):
    hexes = ['0', '1', '2', '3', '4', '5']
    def generate(self):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if roll <= 4:
            return '0'
        else:
            roll = mydice.roll(2, 6)
            if roll == 2 or roll == 3:
                return '1'
            elif roll == 4 or roll == 5:
                return '2'
            elif roll == 6 or roll == 7:
                return '3'
            elif roll == 8 or roll == 9 or roll == 10:
                return '4'
            else:
                return '5'
            

class PlanetoidBelts(Element):
    hexes = ['0', '1', '2']
    def generate(self):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if roll <= 7:
            return '0'
        else:
            roll = mydice.roll(2, 6)
            if roll >= 7:
                return '1'
            else:
                return '2'

class Star:
    sizes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'D']
    types = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    decimals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    def __init__(self, atmosphere, population):
        """ self.type is a reserved word in python """
        self.typeThrow = 0
        self.sizeThrow = 0
        self.stellarType = self.generateType(atmosphere, population)
        self.decimal = self.generateDecimal()
        self.size = self.generateSize(atmosphere, population, self.stellarType, self.decimal)

    def getTypeThrow(self):
        return self.typeThrow

    def getSizeThrow(self):
        return self.sizeThrow

    def getString(self):
        return "%c%c %s" % (self.stellarType, self.decimal, self.size)

    def generateType(self, atmosphere, population):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if (atmosphere.getHex() >= '4' and atmosphere.getHex() <= '9') or population.getHex() >= '8':
            roll += 4
        self.typeThrow = roll
        if roll <= 2:
            return 'A'
        elif roll <= 7:
            return 'M'
        elif roll == 8:
            return 'K'
        elif roll == 9:
            return 'G'
        else:
            return 'F'

    def generateDecimal(self):
        mydice = dice.Dice()
        roll = mydice.roll(1, 10)
        return self.__class__.decimals[roll - 1]
        
    def generateSize(self, atmosphere, population, stellarType, decimal):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if (atmosphere.getHex() >= '4' and atmosphere.getHex() <= '9') or population.getHex() >= '8':
            roll += 4
        self.sizeThrow = roll
        if roll <= 2:
            base = 'II'
        elif roll == 3:
            base = 'III'
        elif roll == 4:
            base = 'IV'
        elif roll <= 10:
            base = 'V'
        elif roll == 11:
            base = 'VI'
        else:
            base = 'D'

        if base == 'IV':
            if stellarType == 'M':
                base = 'V'
            elif stellarType == 'K' and decimal >= '5':
                base = 'V'
            elif stellarType == 'B' or stellarType == 'A':
                base = 'V'
            elif stellarType == 'F' and decimal <= '4':
                base = 'V'
        return base

class Companion(Star):
    def __init__(self, typeDm, sizeDm, farDm):
        self.typeThrow = 0
        self.sizeThrow = 0
        self.stellarType = self.generateType(typeDm)
        self.decimal = self.generateDecimal()
        self.size = self.generateSize(sizeDm, self.stellarType, self.decimal)
        self.isFar = self.generateIsFar(farDm)

    def generateType(self, typeDm):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        roll += typeDm
        self.typeThrow = roll
        if roll <= 2:
            return 'A'
        elif roll <= 4:
            return 'F'
        elif roll <= 6:
            return 'G'
        elif roll <= 8:
            return 'K'
        else:
            return 'M'
 
    def generateSize(self, sizeDm, stellarType, decimal):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        roll += sizeDm
        self.sizeThrow = roll
        if roll <= 2:
            base = 'II'
        elif roll == 3:
            base = 'III'
        elif roll == 4:
            base = 'IV'
        elif roll <= 10:
            base = 'V'
        elif roll == 11:
            base = 'VI'
        else:
            base = 'D'

        if base == 'IV':
            if stellarType == 'M':
                base = 'V'
            elif stellarType == 'K' and decimal >= '5':
                base = 'V'
            elif stellarType == 'B' or stellarType == 'A':
                base = 'V'
            elif stellarType == 'F' and decimal <= '4':
                base = 'V'
        return base

    def generateIsFar(self, farDm):
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        roll += farDm
        if roll >= 12:
            return True
        else:
            return False

    def getIsFar(self):
        return self.isFar

class Uwp:
    def __init__(self, coordinates=[0, 0], name="Default", settlement="Standard", allegience="Im"):
        self.name = name
        self.coordinates = coordinates
        self.starport = Starport(settlement)
        self.size = Size()
        self.atmosphere = Atmosphere(self.size)
        self.hydrosphere = Hydrosphere(self.size, self.atmosphere)
        self.population = Population()
        self.government = Government(self.population)
        self.law = Law(self.government)
        self.tech = Tech(self.starport, self.size, self.atmosphere, self.hydrosphere, self.population, self.government)
        self.base = Base(self.starport)
        self.tradeCodes = self.getTrades(self.size, self.atmosphere, self.hydrosphere, self.population, self.government, self.law)
        self.zone = Zone(self.starport, self.government, self.law)
        self.populationMultiplier = PopulationMultiplier()
        self.planetoidBelts = PlanetoidBelts()
        self.gasGiants = GasGiants()
        self.allegience = allegience
        self.stars = []
        self.primary = Star(self.atmosphere, self.population)
        self.stars.append(self.primary)
        """ Get companion stars """
        for i in self.getCompanions(self.primary, False):
            self.stars.append(i)
            if i.getIsFar():
                for j in self.getCompanions(i, True):
                    self.stars.append(j)

    def getCoordinates(self):
        return self.coordinates

    def getStarport(self):
        return self.starport.getHex()

    def getCompanions(self, primary, isFar):
        companions = []
        dm = 0
        mydice = dice.Dice()
        roll = mydice.roll(2, 6)
        if isFar:
            roll -= 1
            dm = -4
        if roll >= 8:
            companions.append(Companion(primary.getTypeThrow(), primary.getSizeThrow(), dm))
        if roll >= 12:
            dm += 4
            companions.append(Companion(primary.getTypeThrow(), primary.getSizeThrow(), dm))
        return companions

    def getTrades(self, size, atmosphere, hydrosphere, population, government, law):
        codes = []
        if self.getAgricultural(atmosphere, hydrosphere, population):
            codes.append("Ag")
        if self.getAsteroid(size, atmosphere, hydrosphere):
            codes.append("As")
        if self.getBarren(population, government, law):
            codes.append("Ba")
        if self.getDesert(atmosphere, hydrosphere):
            codes.append("De")
        if self.getFluidOceans(size, atmosphere):
            codes.append("Fl")
        if self.getHighPopulation(population):
            codes.append("Hi")
        if self.getIceCapped(atmosphere, hydrosphere):
            codes.append("Ic")
        if self.getIndustrial(atmosphere, population):
            codes.append("In")
        if self.getLowPopulation(population):
            codes.append("Lo")
        if self.getNonAgricultural(atmosphere, hydrosphere, population):
            codes.append("Na")
        if self.getNonIndustrial(population):
            codes.append("Ni")
        if self.getPoor(atmosphere, hydrosphere):
            codes.append("Po")
        if self.getRich(atmosphere, population, government):
            codes.append("Ri")
        if self.getVacuum(size, atmosphere, hydrosphere):
            codes.append("Va")
        if self.getWaterWorld(hydrosphere):
            codes.append("Wa")
        return codes

    def getAgricultural(self, atmosphere, hydrosphere, population):
        if (atmosphere.getHex() >= '4' and atmosphere.getHex() <= '9') and \
           (hydrosphere.getHex() >= '4' and hydrosphere.getHex() <= '8') and \
           (population.getHex() >= '5' and population.getHex() <= '7'):
            return True
        else:
            return False

    def getAsteroid(self, size, atmosphere, hydrosphere):
        if (size.getHex() == '0' and atmosphere.getHex() == '0' and hydrosphere.getHex() == '0'):
            return True
        else:
            return False

    def getBarren(self, population, government, law):
        if (population.getHex() == '0' and government.getHex() == '0' and law.getHex() == '0'):
            return True
        else:
            return False

    def getDesert(self, atmosphere, hydrosphere):
        if (atmosphere.getHex() >= '2' and hydrosphere.getHex() == '0'):
            return True
        else:
            return False

    def getFluidOceans(self, size, atmosphere):
        if (size.getHex() >= 'A' and atmosphere.getHex() >= '1'):
            return True
        else:
            return False

    def getHighPopulation(self, population):
        if population.getHex() >= '9':
            return True
        else:
            return False

    def getIceCapped(self, atmosphere, hydrosphere):
        if (atmosphere.getHex() <= '1' and hydrosphere >= '1'):
            return True
        else:
            return False
    def getIndustrial(self, atmosphere, population):
        if (((atmosphere.getHex() >= '2' and atmosphere.getHex() <= '4') or \
             atmosphere.getHex() == '7' or \
             atmosphere.getHex() == '9') and \
            population.getHex() >= '9'):
            return True
        else:
            return False

    def getLowPopulation(self, population):
        if population.getHex() <= '3':
            return True
        else:
            return False

    def getNonAgricultural(self, atmosphere, hydrosphere, population):
        if(atmosphere.getHex() <= '3' and hydrosphere.getHex() <= '3' and population.getHex() >= '6'):
            return True
        else:
            return False

    def getNonIndustrial(self, population):
        if population.getHex() <= '6':
            return True
        else:
            return False

    def getPoor(self, atmosphere, hydrographics):
        if (atmosphere.getHex() >= '2' and atmosphere.getHex() <= '5') and hydrographics.getHex() <= '3':
            return True
        else:
            return False

    def getRich(self, atmosphere, population, government):
        if (atmosphere.getHex() == '6' or atmosphere.getHex() == '8') and \
           (population.getHex() >= '6' and population.getHex() <= '8') and \
           (government.getHex() >= '4' and government.getHex() <= '9'):
            return True
        else:
            return False

    def getVacuum(self, size, atmosphere, hydrosphere):
        if atmosphere.getHex() == '0' and not (size.getHex() == '0' and hydrosphere.getHex() == '0'):
            return True
        else:
            return False

    def getWaterWorld(self, hydrosphere):
        if hydrosphere.getHex() == 'A':
            return True
        else:
            return False

    def getString(self):
        return self.sec()

    def sec(self):
        trades = " ".join(self.tradeCodes)
        starStrings = []
        for star in self.stars:
            starStrings.append(star.getString());
        starString = " ".join(starStrings)
        ret = "%-18s %02d%02d %c%c%c%c%c%c%c-%c %c %-14s %c  %c%c%c %-2s %-20s" % (
                self.name, self.coordinates[0], self.coordinates[1], 
                self.starport.getHex(), self.size.getHex(), self.atmosphere.getHex(), 
                self.hydrosphere.getHex(), self.population.getHex(), self.government.getHex(), 
                self.law.getHex(), self.tech.getHex(), 
                self.base.getHex(), trades, self.zone.getHex(), 
                self.populationMultiplier.getHex(), self.planetoidBelts.getHex(), self.gasGiants.getHex(),
                self.allegience, starString
            )
        return ret

    def get_coordinates(self):
        return this.coordinates


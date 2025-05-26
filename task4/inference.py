# inference.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import itertools
import random
import busters
import game

from util import manhattanDistance, raiseNotDefined


class DiscreteDistribution(dict):
    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

    def copy(self):
        return DiscreteDistribution(dict.copy(self))

    def argMax(self):
        if len(self.keys()) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def total(self):
        return float(sum(self.values()))

    def normalize(self):
        total = self.total()
        if total == 0:
            return
        for key in self.keys():
            self[key] /= total

    def sample(self):
        total = self.total()
        if total == 0:
            raise Exception("Cannot sample from an empty distribution.")
        target = random.uniform(0, total)
        cumulative = 0.0
        for key, value in self.items():
            cumulative += value
            if cumulative >= target:
                return key


class InferenceModule:
    def __init__(self, ghostAgent):
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = []

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistributionHelper(self, gameState, pos, index, agent):
        try:
            jail = self.getJailPosition()
            gameState = self.setGhostPosition(gameState, pos, index + 1)
        except TypeError:
            jail = self.getJailPosition(index)
            gameState = self.setGhostPositions(gameState, pos)
        pacmanPosition = gameState.getPacmanPosition()
        ghostPosition = gameState.getGhostPosition(index + 1)
        dist = DiscreteDistribution()
        if pacmanPosition == ghostPosition:
            dist[jail] = 1.0
            return dist
        pacmanSuccessorStates = game.Actions.getLegalNeighbors(pacmanPosition, gameState.getWalls())
        if ghostPosition in pacmanSuccessorStates:
            mult = 1.0 / float(len(pacmanSuccessorStates))
            dist[jail] = mult
        else:
            mult = 0.0
        actionDist = agent.getDistribution(gameState)
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            if successorPosition in pacmanSuccessorStates:
                denom = float(len(actionDist))
                dist[jail] += prob * (1.0 / denom) * (1.0 - mult)
                dist[successorPosition] = prob * ((denom - 1.0) / denom) * (1.0 - mult)
            else:
                dist[successorPosition] = prob * (1.0 - mult)
        return dist

    def getPositionDistribution(self, gameState, pos, index=None, agent=None):
        if index == None:
            index = self.index - 1
        if agent == None:
            agent = self.ghostAgent
        return self.getPositionDistributionHelper(gameState, pos, index, agent)

    def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, jailPosition):
        if ghostPosition == jailPosition:
            return 1.0 if noisyDistance is None else 0.0
        if noisyDistance is None:
            return 0.0
        return busters.getObservationProbability(noisyDistance, manhattanDistance(pacmanPosition, ghostPosition))

    def setGhostPosition(self, gameState, ghostPosition, index):
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[index] = game.AgentState(conf, False)
        return gameState

    def setGhostPositions(self, gameState, ghostPositions):
        for index, pos in enumerate(ghostPositions):
            conf = game.Configuration(pos, game.Directions.STOP)
            gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
        return gameState

    def observe(self, gameState):
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index:
            obs = distances[self.index - 1]
            self.obs = obs
            self.observeUpdate(obs, gameState)

    def initialize(self, gameState):
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.allPositions = self.legalPositions + [self.getJailPosition()]
        self.initializeUniformly(gameState)

    def initializeUniformly(self, gameState):
        self.beliefs = DiscreteDistribution()
        for p in self.legalPositions:
            self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observeUpdate(self, observation, gameState):
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()
        for position in self.allPositions:
            self.beliefs[position] *= self.getObservationProb(observation, pacmanPosition, position, jailPosition)
        self.beliefs.normalize()

    def elapseTime(self, gameState):
        newBeliefs = DiscreteDistribution()
        for oldPos in self.allPositions:
            newPosDist = self.getPositionDistribution(gameState, oldPos)
            for newPos, prob in newPosDist.items():
                newBeliefs[newPos] += prob * self.beliefs[oldPos]
        self.beliefs = newBeliefs
        self.beliefs.normalize()

    def getBeliefDistribution(self):
        return self.beliefs


class ExactInference(InferenceModule):
    def initializeUniformly(self, gameState):
        self.beliefs = DiscreteDistribution()
        for p in self.legalPositions:
            self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observeUpdate(self, observation, gameState):
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()
        for position in self.allPositions:
            self.beliefs[position] *= self.getObservationProb(observation, pacmanPosition, position, jailPosition)
        self.beliefs.normalize()

    def elapseTime(self, gameState):
        newBeliefs = DiscreteDistribution()
        for oldPos in self.allPositions:
            newPosDist = self.getPositionDistribution(gameState, oldPos)
            for newPos, prob in newPosDist.items():
                newBeliefs[newPos] += prob * self.beliefs[oldPos]
        self.beliefs = newBeliefs
        self.beliefs.normalize()

    def getBeliefDistribution(self):
        return self.beliefs


class ParticleFilter(InferenceModule):
    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent)
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initializeUniformly(self, gameState):
        self.particles = []
        numParticles = self.numParticles
        positions = self.legalPositions
        while len(self.particles) < numParticles:
            self.particles += positions
        self.particles = self.particles[:numParticles]

    def observeUpdate(self, observation, gameState):
        pacmanPosition = gameState.getPacmanPosition()
        jailPosition = self.getJailPosition()
        beliefDistribution = DiscreteDistribution()

        for particle in self.particles:
            beliefDistribution[particle] += self.getObservationProb(observation, pacmanPosition, particle, jailPosition)

        if beliefDistribution.total() == 0:
            self.initializeUniformly(gameState)
        else:
            self.particles = [beliefDistribution.sample() for _ in range(self.numParticles)]

    def elapseTime(self, gameState):
        newParticles = []
        for oldPos in self.particles:
            newPosDist = self.getPositionDistribution(gameState, oldPos)
            newParticles.append(newPosDist.sample())
        self.particles = newParticles

    def getBeliefDistribution(self):
        beliefDistribution = DiscreteDistribution()
        for particle in self.particles:
            beliefDistribution[particle] += 1
        beliefDistribution.normalize()
        return beliefDistribution


class JointParticleFilter(ParticleFilter):
    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def initialize(self, gameState, legalPositions):
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeUniformly(gameState)

    def initializeUniformly(self, gameState):
        self.particles = []
        possibleParticles = list(itertools.product(self.legalPositions, repeat=self.numGhosts))
        random.shuffle(possibleParticles)
        numParticles = self.numParticles
        while len(self.particles) < numParticles:
            self.particles += possibleParticles
        self.particles = self.particles[:numParticles]

    def addGhostAgent(self, agent):
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1)

    def observe(self, gameState):
        observation = gameState.getNoisyGhostDistances()
        self.observeUpdate(observation, gameState)

    def observeUpdate(self, observation, gameState):
        pacmanPosition = gameState.getPacmanPosition()
        beliefDistribution = DiscreteDistribution()

        for particle in self.particles:
            weight = 1.0
            for i in range(self.numGhosts):
                jailPosition = self.getJailPosition(i)
                weight *= self.getObservationProb(observation[i], pacmanPosition, particle[i], jailPosition)
            beliefDistribution[particle] += weight

        if beliefDistribution.total() == 0:
            self.initializeUniformly(gameState)
        else:
            self.particles = [beliefDistribution.sample() for _ in range(self.numParticles)]

    def elapseTime(self, gameState):
        newParticles = []
        for oldParticle in self.particles:
            newParticle = list(oldParticle)
            for i in range(self.numGhosts):
                newPosDist = self.getPositionDistribution(gameState, oldParticle[i], i, self.ghostAgents[i])
                newParticle[i] = newPosDist.sample()
            newParticles.append(tuple(newParticle))
        self.particles = newParticles

# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()


class MarginalInference(InferenceModule):
    def initializeUniformly(self, gameState):
        if self.index == 1:
            jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observe(self, gameState):
        if self.index == 1:
            jointInference.observe(gameState)

    def elapseTime(self, gameState):
        if self.index == 1:
            jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        jointDistribution = jointInference.getBeliefDistribution()
        dist = DiscreteDistribution()
        for t, prob in jointDistribution.items():
            dist[t[self.index - 1]] += prob
        return dist

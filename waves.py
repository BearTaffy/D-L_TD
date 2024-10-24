import viz
import vizact
from creeps import Creep, creeps, creepPath


class WaveManager:
    def __init__(self):
        self.currentWave = 0
        self.creepsToSpawn = 0
        self.spawnInterval = 1.0
        self.waveInterval = 15.0
        self.isWaveActive = False
        self.lastSpawnTime = 0
        self.waveStartTime = 0
        self.difficultyMultiplier = 1.0

    def startWave(self):
        self.currentWave += 1
        self.isWaveActive = True
        self.waveStartTime = viz.tick()

        self.creepsToSpawn = 5 + (2 * self.currentWave)

        if self.currentWave % 5 == 0:
            self.difficultyMultiplier += 0.2

        print(f"Wave {self.currentWave} started!")

    def update(self):
        current_time = viz.tick()

        if not self.isWaveActive:
            if current_time - self.waveStartTime >= self.waveInterval:
                self.startWave()

        elif self.creepsToSpawn > 0:
            if current_time - self.lastSpawnTime >= self.spawnInterval:
                self.spawnCreep()
                self.lastSpawnTime = current_time

        elif len(creeps) == 0 and self.creepsToSpawn == 0:
            self.isWaveActive = False
            self.waveStartTime = current_time
            print(f"Wave {self.currentWave} complete!")

    def spawnCreep(self):
        if self.creepsToSpawn > 0:
            newCreep = Creep(creepPath)
            newCreep.model.setPosition(creepPath[0])

            newCreep.health = int(100 * self.difficultyMultiplier)
            newCreep.speed = 0.1 * self.difficultyMultiplier

            creeps.append(newCreep)
            self.creepsToSpawn -= 1


wave_manager = WaveManager()


def updateWaveSystem():
    wave_manager.update()

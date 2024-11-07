import viz
import vizact
import random

import infoScreen
from creeps import Creep, creeps, creepPath, creepPathShort, creepTypes

gameReady = False


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
        self.setupUI()

    def initializeGame(self):
        global gameReady
        self.currentWave = 0
        self.creepsToSpawn = 0
        self.isWaveActive = False
        self.waveStartTime = viz.tick()
        self.lastSpawnTime = 0
        self.difficultyMultiplier = 1.0
        gameReady = True
        self.updateUI()

    def setupUI(self):
        self.panel = viz.addText("")
        self.panel.alignment(viz.ALIGN_LEFT_TOP)
        self.panel.setBackdrop(viz.BACKDROP_OUTLINE)
        self.panel.alpha(0.7)
        self.panel.setPosition(19, 7, 3)
        self.panel.setScale(0.7, 0.7, 0.7)
        self.panel.billboard(viz.BILLBOARD_VIEW)
        self.panel.depthFunc(viz.GL_ALWAYS)

        self.updateUI()

    def updateUI(self):
        if self.isWaveActive:
            status = f"WAVE {self.currentWave} IN PROGRESS\n"
            status += f"Remaining Creeps: {self.creepsToSpawn + len(creeps)}\n"
        else:
            time_until_next = max(
                0, self.waveInterval - (viz.tick() - self.waveStartTime)
            )
            status = f"WAVE {self.currentWave} COMPLETE\n"
            status += f"Next Wave in: {time_until_next:.1f}s\n"

        status += f"\nDifficulty: {self.difficultyMultiplier:.1f}x"
        self.panel.message(status)

    def startWave(self):
        self.currentWave += 1
        self.isWaveActive = True
        self.waveStartTime = viz.tick()

        self.creepsToSpawn = 4 + (3 * self.currentWave)

        if self.currentWave % 2 == 0:
            self.difficultyMultiplier += 0.15

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

    def creepPool(self):
        if self.difficultyMultiplier < 1.3:
            types = list(creepTypes.keys())[:1]
        elif self.difficultyMultiplier >= 1.3:
            types = list(creepTypes.keys())[:2]
        elif self.difficultyMultiplier <= 1.6:
            types = list(creepTypes.keys())[:-1]
        else:
            types = list(creepTypes.keys())
        return types

    def spawnCreep(self):
        if self.creepsToSpawn > 0:
            types = self.creepPool()

            strongCreepChance = min(0.8, (self.difficultyMultiplier - 1.0) * 2)

            if random.random() < strongCreepChance and len(types) > 1:
                creepName = random.choice(types[len(types) // 2 :])
            else:
                creepName = random.choice(types)

            creepType = creepTypes[creepName]
            path = creepPathShort if random.random() < 0.2 else creepPath

            newCreep = Creep(path, creepType)
            newCreep.health = int(newCreep.health * self.difficultyMultiplier)
            newCreep.maxHealth = newCreep.health
            newCreep.damage = int(newCreep.damage * self.difficultyMultiplier)

            newCreep.model.setPosition(path[0])

            creeps.append(newCreep)
            self.creepsToSpawn -= 1


class BaseHealth:
    def __init__(self):
        self.maxHealth = 150
        self.health = self.maxHealth
        self.setupUI()

    def setupUI(self):
        self.panel = viz.addText("")
        self.panel.alignment(viz.ALIGN_RIGHT_TOP)
        self.panel.setBackdrop(viz.BACKDROP_OUTLINE)
        self.panel.alpha(0.7)
        self.panel.setPosition(-14, 2, 2.5)
        self.panel.setScale(0.7, 0.7, 0.7)
        self.panel.billboard(viz.BILLBOARD_VIEW)
        self.panel.depthFunc(viz.GL_ALWAYS)
        self.updateUI()

    def reset(self):
        self.health = self.maxHealth
        self.updateUI()

    def takeDamage(self, damage):
        global gameReady
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print("Game Over - Base Destroyed!")
            infoScreen.gameOver()
            gameReady = False
        self.updateUI()

    def updateUI(self):
        status = f"HOME BASE\nHealth: {self.health}"
        self.panel.message(status)


base_health = BaseHealth()

wave_manager = WaveManager()


def updateWaveSystem():
    if gameReady:
        wave_manager.update()
        wave_manager.updateUI()

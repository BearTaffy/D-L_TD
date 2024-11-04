import viz
import vizact
import random
from creeps import Creep, creeps, creepPath, creepPathShort, creepTypes
from infoScreen import startGame, gameIsStart



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
            creep_type_name = random.choice(list(creepTypes.keys()))
            creep_type = creepTypes[creep_type_name]

            path = creepPathShort if random.random() < 0.2 else creepPath

            newCreep = Creep(path, creep_type)
            newCreep.model.setPosition(path[0])

            creeps.append(newCreep)
            self.creepsToSpawn -= 1


class BaseHealth:
    def __init__(self):
        self.health = 100
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

    def updateUI(self):
        status = f"HOME BASE\nHealth: {self.health}"
        self.panel.message(status)

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print("Game Over - Base Destroyed!")
        self.updateUI()


base_health = BaseHealth()

wave_manager = WaveManager()


def updateWaveSystem():
    if gameIsStart == True:
        wave_manager.update()
        wave_manager.updateUI()
        


import time
import project.state as state
import project.engine as engine

machines=[{'id':'Mixer01'},{'id':'Conveyor03'}]
state.init_all(machines)

while True:
    engine.run_cycle()
    time.sleep(2)

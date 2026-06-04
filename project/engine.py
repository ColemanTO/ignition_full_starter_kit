
import project.state as state
import project.solver_client as solver

def run_cycle():
    s = state.get_all()
    plan = solver.get_plan(s)

    for action in plan.get('schedule', []):
        print('Applying:', action)

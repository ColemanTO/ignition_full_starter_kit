
import datetime

import project.state as state
import project.solver_client as solver

def run_cycle():
    s = state.get_all()
    plan = solver.get_plan(s)

    for action in plan.get('schedule', []):
        print('Applying:', action)
        machine = action.get('machine')
        if machine not in s:
            continue

        op = action.get('action', '').upper()
        if op == 'START':
            s[machine]['state'] = 'READY'
            s[machine]['status'] = 'RUNNING'
        elif op == 'STOP':
            s[machine]['state'] = 'IDLE'
            s[machine]['status'] = 'STOPPED'
        else:
            s[machine]['status'] = f'UNKNOWN ACTION: {op}'

        s[machine]['lastUpdate'] = datetime.datetime.now()


# Simplified state store for Ignition
state = {}

def init_all(machines):
    import datetime
    for m in machines:
        state[m['id']] = {
            'state':'IDLE',
            'status':'UNKNOWN',
            'lastUpdate': datetime.datetime.now()
        }

def get_all():
    return state

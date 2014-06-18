
from bottle import route, run, static_file
from math import ceil

from redis.sentinel import Sentinel

#Slave/Master distribution
sentinel = Sentinel('TODO: Get some Redis instances in Amazons AWS')
master = sentinel.master_for('.')
slave = sentinel.slave_for('.')


@route('/')
def home():
    return static_file('index.html', '..')


@route('/get/stats')
def getStats():
    return generate_json()


@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='..')


def generate_json():
    # Pipeline all the requests to the SLAVE (All read)
    pipe = slave.pipeline()
    #Pipeline returns all responses in a list
    responselist = pipe.hget('global', 'kills').\
        hget('global', 'deaths').\
        hget('global', 'joins').\
        hget('global', 'blocks-placed').\
        hget("global", "block-breaks").\
        hget("global", "time-played").\
        hget("global", "rounds-played").\
        hget("global", "players-revived").execute()

    #Couldn't think of a better way here...
    for i, j in enumerate(responselist):

        if i == 0:
            kills = j
        if i == 1:
            deaths = j
        if i == 2:
            joins = j
        if i == 3:
            placed = j
        if i == 4:
            breaks = j
        if i == 5:
            time = convertMillis(float(j))
        if i == 6:
            rounds = j
        if i == 7:
            revived = j
    #Make our dictionary...
    data = {
        "Kills": kills,
        "Deaths": deaths,
        "Joins": joins,
        "Blocks Placed": placed,
        "Blocks Broke": breaks,
        "Time Played": str(time) + " days",
        "Rounds Played": rounds,
        "Players Revived": revived}
    #Return it as JSON
    return data


def convertMillis(l):
    #days
    num = (l / 1000.0) / 60.0 / 60 / 24
    #round up to the nearest hundredth place
    return ceil(num * 100) / 100.0


run(host='localhost', port=8080)

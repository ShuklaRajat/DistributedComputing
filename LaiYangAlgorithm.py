from collections import OrderedDict

numProcesses = 2
processIdentifier = ['X', 'Y']

initialAmount = dict()
initialAmount['X'] = 800
initialAmount['Y'] = 200

# updatedAmount = [[]]
# updatedAmount = [[800], [200]]
updatedAmount = dict()
updatedAmount = {               # TODO: Ensure that updateAmount[processName] is an OrderedDictionary
    'X' : {
        't1' : 800
    },
    'Y': {
        't1': 200
    }
}

transaction_send = OrderedDict()
transaction_receive = OrderedDict()
#transaction_send initiated by X of amount 20 between time period t1 and t2. The amount reaches process 'Y between time
# period t2 and t3.
transaction_send['X'] = [[20, 't1', 't2', 'Y']]


transaction_receive['Y'] = [[20, 't2', 't3', 'X']]

transaction_send['X'].append([30, 't2', 't3', 'Y'])
transaction_receive['Y'].append([30, 't6', 't7', 'X'])

transaction_send['X'].append([10, 't3', 't4', 'Y'])
transaction_receive['Y'].append([10, 't5', 't6', 'X'])

transaction_send['Y'] = [[30, 't4', 't5', 'X']]
transaction_receive['X'] = [[30, 't6', 't7', 'Y']]

transaction_send['Y'].append([20, 't7', 't8', 'X'])
transaction_receive['X'].append([20, 't8', 't9', 'Y'])

lastTimeArr = {'X': [None, None, None, None, None, 30, None, 20],
                'Y': [None, 20, None, None, 10, 30]
               }

#updateAmount processing. Initialization of time till the maximum available time. (Here, assumed from t1 to t9.)
for process in processIdentifier:
    for timeint in range(1, 10):
        if 't'+str(timeint) in updatedAmount[process].keys():
            continue
        updatedAmount[process]['t'+str(timeint)] = updatedAmount[process]['t'+str(timeint-1)]

print("Pre-processing for updateAmount: ", updatedAmount)


for process in processIdentifier:
    for i in range(2, 10):
        time = 't'+str(i)
        flag = 0
        for timestamp in transaction_send[process]:
            if time in timestamp and time == timestamp[2]:
                updatedAmount[process][time] = updatedAmount[process]['t'+str(i-1)] - \
                                                timestamp[0]
                flag = 1
        for timestamp in transaction_receive[process]:
            if time in timestamp and time == timestamp[2]:
                updatedAmount[process][time] = updatedAmount[process]['t'+str(i-1)] + \
                                                timestamp[0]
                flag = 1

        if flag != 1:
            updatedAmount[process][time] = updatedAmount[process]['t' + str(i - 1)]

print("updatedAmount after all send and receive:\n\t", updatedAmount)




snapshotAt = ['X', 't3', 't3']

# Check in transaction_send['X'] where is 't3'. Once found, turn the corresponding Y process to red

processColor = dict()
# processColor['Y'] = ['Red', 't5', 't6']  #This needs to be computed programatically

for i in range(len(transaction_send[snapshotAt[0]])):
    if transaction_send[snapshotAt[0]][i][1] == snapshotAt[1]:
        processColor[transaction_send[snapshotAt[0]][i][3]] \
            = ['Red',
                transaction_receive[transaction_send[snapshotAt[0]][i][3]][i][1],
                transaction_receive[transaction_send[snapshotAt[0]][i][3]][i][2]]

print("processColor:\n\t", processColor)


channel_send = dict()
channel_receive = dict()

"""
Below logic is only for the process which has initiated the global snapshot recording.
"""
snapshotAtTimeNumeric = int(snapshotAt[1].lstrip('t'))
# print(snapshotAtTimeNumeric)

for processName in processIdentifier:
    for i in range(len(transaction_send[processName])):

        if int(transaction_send[processName][i][1].lstrip('t')) < snapshotAtTimeNumeric or \
            (int(transaction_send[processName][i][1].lstrip('t')) == int(transaction_send[processName][i][2].lstrip('t'))
             == snapshotAtTimeNumeric):

            if processName not in channel_send.keys():
                channel_send[processName] = []

            channel_send[processName].append(transaction_send[processName][i][0])

print(channel_send)
print(sum(channel_send['X']))

"""
Below logic is to calculate the channel state during SEND for the processes apart from the process that initiated the global snapshot recording.
"""


for processName in processIdentifier:
    if processName != snapshotAt[0]:
        for i in range(len(transaction_send[processName])):

            if int(transaction_send[processName][i][1].lstrip('t')) < int(processColor[processName][2].lstrip('t')) or \
                (int(transaction_send[processName][i][1].lstrip('t'))
                 == int(transaction_send[processName][i][2].lstrip('t'))
                 == int(processColor[processName][2].lstrip('t'))):

                if processName not in channel_send.keys():
                    channel_send[processName] = []

                channel_send[processName].append(transaction_send[processName][i][0])


print("channel_send:\n\t", channel_send)


"""
Below logic is for the process which initiates the global state recording.
"""
processName = snapshotAt[0]
for i in range(len(transaction_receive[processName])):

    if int(transaction_receive[processName][i][2].lstrip('t')) < snapshotAtTimeNumeric or \
        (int(transaction_receive[processName][i][2].lstrip('t')) == int(transaction_receive[processName][i][2].lstrip('t'))
         == snapshotAtTimeNumeric):

        if processName not in channel_receive.keys():
            channel_receive[processName] = []

        channel_receive[processName].append(transaction_receive[processName][i][0])

print("channel_receive state before the snapshot :\n\t", channel_receive)


"""
Below logic is for all the processes except for the process that initiated the global snapshot recording.
"""
for processName in processIdentifier:
    if processName != snapshotAt[0]:
        for i in range(len(transaction_receive[processName])):
            if int(transaction_receive[processName][i][2].lstrip('t')) < int(processColor[processName][2].lstrip('t')) or \
                (int(transaction_receive[processName][i][1].lstrip('t'))
                 == int(transaction_receive[processName][i][2].lstrip('t'))
                 == int(processColor[processName][2].lstrip('t'))):

                if processName not in channel_receive.keys():
                    channel_receive[processName] = []

                channel_receive[processName].append(transaction_receive[processName][i][0])

print("channel_receive state before the Process i turned RED:\n\t", channel_receive)






























from collections import OrderedDict

numProcesses = 2
processIdentifier = ['X', 'Y']

initialAmount = dict()
initialAmount['X'] = 800
initialAmount['Y'] = 200

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

print(transaction_send)

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

# print(processColor)


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

# print(channel_send)
# print(sum(channel_send['X']))

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


print(channel_send)



# for processName in processIdentifier:
processName = snapshotAt[0]
for i in range(len(transaction_receive[processName])):

    if int(transaction_receive[processName][i][2].lstrip('t')) < snapshotAtTimeNumeric or \
        (int(transaction_receive[processName][i][2].lstrip('t')) == int(transaction_receive[processName][i][2].lstrip('t'))
         == snapshotAtTimeNumeric):

        if processName not in channel_receive.keys():
            channel_receive[processName] = []

        channel_receive[processName].append(transaction_receive[processName][i][0])


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


print(channel_receive)





























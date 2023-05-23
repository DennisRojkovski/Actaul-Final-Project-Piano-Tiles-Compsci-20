capitals = {'Russia': 'Kiev', 'Canada': 'Ottowa'}
capitals['Russia'] = 'Moscow'
print(capitals)
#Prints 'Russia': 'Moscow', 'Canada': 'Ottowa'
capitals.pop('Canada')
print(capitals)
#Prints 'Russia': 'Moscow'
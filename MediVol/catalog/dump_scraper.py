dump = open('dump.txt')
filtered_dump = file('filtered_dump.txt', 'w')
count = 0
data_map = dict()
for line in dump:
    item_data = line.split('	')
    split_data = item_data[1].split(':')
    if len(split_data) > 1:
        if split_data[0] in data_map.keys():
            data_map[split_data[0]].append(split_data[1])
        else:
            data_map[split_data[0]] = [split_data[1]]
        count = count + 1
print count
print len(data_map.keys())
for key in data_map.keys():
    filtered_dump.write(key+":\n")
    for data in data_map[key]:
        filtered_dump.write("  " + data.strip() + "\n")
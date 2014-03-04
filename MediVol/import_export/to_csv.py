def to_csv_from_array(array):
	filtered_values = []
        for value in array:
            filtered_values.append(value.replace(',', '<CMA>').replace('\n', '<RET>'))
        return ','.join(filtered_values)

def to_array_from_csv(csv):
	values = csv.split(",")
    filtered_values = []
    for value in values:
        filtered_values.append(value.replace('<CMA>', ',').replace('<RET>', '\n'))
    return filtered_values
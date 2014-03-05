def to_csv_from_array(array):
    filtered_values = []
    for value in array:
        filtered_values.append(str(value).replace(',', '<CMA>').replace('\n', '<RET>'))
    return ','.join(filtered_values)

def to_array_from_csv(csv):
    values = csv.split(",")
    filtered_values = []
    for value in values:
    	filtered_value = value
    	filtered_value = filtered_value.replace('<CMA>', ',')
    	filtered_value = filtered_value.replace('<RET>', '\n')
    	if filtered_value == 'None':
    		filtered_value = None
        filtered_values.append(filtered_value)
    return filtered_values
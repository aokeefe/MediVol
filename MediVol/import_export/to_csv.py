def to_csv_from_array(array):
	filtered_values = []
        for value in array:
            filtered_values.append(value.replace(',', '<CMA>').replace('\n', ''))
        return ','.join(filtered_values)
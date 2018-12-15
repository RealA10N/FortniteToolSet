

def generate_table_list(items_in_row, num_of_rows, deafult_value=None):
    list = []
    temp_list = []
    for i in range(num_of_rows):
        for ii in range(items_in_row):
            temp_list.append(deafult_value)
        list.append(temp_list)
        temp_list = []
    return list

list = ['#f442d9', '#ffffff', '#ef3d1a', '#192fef', '#f9d504', '#000000',]
featured_list = [False, True, False, False, False, True]

items_in_line = 3
table = generate_table_list(3,4)
print(table)



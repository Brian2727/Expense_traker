




def Category_Spent_Serializer(data):
    serialized_data = {}

    for category_dict_sum in data:
        serialized_data[category_dict_sum['category']] = category_dict_sum['sum']
    print(serialized_data)
    return serialized_data
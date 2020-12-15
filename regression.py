import access

def do_linear_regression(type_id):
    matrix = access.item_matrix(type_id) # item id of abyssal magstab

    # print the data just to show what it looks like
    for vector in matrix:
        print(vector)

    # code for linear regression goes here
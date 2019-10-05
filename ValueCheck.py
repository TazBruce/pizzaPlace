# noinspection PyBroadException
# Function that checks value for set parameters
def valuecheck(value, string, minimum, maximum):
    # If 'string' parameter is set to True test for character count
    if string:
        try:
            # If string character count is between set range accept value
            if minimum <= len(value) <= maximum:
                print("ACCEPT STRING")
            else:
                print("POPUP")
        # If function fails to test character count value is invalid
        except:
            print("BREAK")
    # If 'string' parameter is set to False test that integer is between range
    else:
        try:
            if minimum <= value <= maximum:
                print("ACCEPT NUMBER")
            else:
                print("POPUP")
        # If function fails to test value is between integer range value is invalid
        except:
            print("BREAK")

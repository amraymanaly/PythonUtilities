#!/usr/bin/python3
def get_input(msg, err_msg='', data=str, only=[], max_length=200, opt_data=str):
    '''
    msg: the message displayed to the user expecting him for input ..
    err_msg: the message displayed to the user if his input didn't match the "data" type (an empty string by default)
    data: the type of data the user is going to enter (str by default)
    only: user input has to be found in this list, if not, user will be prompted automatically. If empty, has no effect (empty by default)
    max_length: maximum length allowed for input, if exceeded, user will be prompted (200 by default)
    opt_data: an optional datatype that original input (str) needs to support conversion to.
        If conversion failed, valid input will be requested then.
        This is useful when you want to get the input's original form but make sure conversion is supported, to ensure valid data ..
        For example, you want to get an str that could be converted to an int, but need to get the zeros on the left side ..
        which would normally get ommited if actually converted to int ..
    '''
    while True:
        try:
            for el in only: # checking if all elements in the "only" list is same in type with "data" (diagnostic)
                if not isinstance(el, data):
                    raise TypeError('Not all elements in the "only" list is an instance of "data (%s)"' % data)

            choice = input(msg) # getting choice ..
            choice2 = opt_data(choice) # if error, ValueError will be trigerred
            choice = data(choice) # required datatype ..

            if not choice in only and len(only) > 0: # using the "only" list ..
                print('Expected: {0}'.format(', '.join([str(data(o)) for o in only])))
                continue

            if len(str(choice)) > max_length: # evaluating length bounds ..
                print('Maximum length: %d' % max_length)
                continue

            break
        except ValueError:
            print(err_msg)
    return choice

def to_qmp(namespace):
    '''
    Converts a parsed Namespace to a QMP formatted dictionary

            Parameters: 
                    namespace (Namespace): a Nampespace object containing one unlinked 
                                           argument and any number of linked ones

            Returns: 
                    qmp (dict): a dictionary which takes the unlinked object and makes it
                                the command in QMP format, and makes the linked arguments
                                into the arguments to the command in QMP format
    '''
    result = {}
    for name in vars(namespace):
        if name == 'command':
            result["execute"] = vars(namespace)[name]
        elif 'arguments' not in result:
            result["arguments"] = {name: vars(namespace)[name]}
        else:
            result["arguments"][name] =  vars(namespace)[name]

    return result
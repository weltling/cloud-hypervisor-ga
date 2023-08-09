import json


def to_qmp(namespace):
    '''
    Converts a parsed Namespace to a QMP formatted dictionary

            Parameters:
                    namespace (Namespace): a Nampespace object
                                           containing one unlinked
                                           argument and any number
                                           of linked ones

            Returns:
                    qmp (dict): a dictionary which takes the
                                unlinked object and makes it
                                the command in QMP format, and
                                makes the linked arguments
                                into the arguments to the command
                                in QMP format
    '''
    result = {}
    for name in vars(namespace):
        value = vars(namespace)[name]
        if isinstance(value, str) and "," in value:
            value = value.split(",")
        if value is not None:
            if name == 'command':
                result["execute"] = value
            elif 'arguments' not in result:
                result["arguments"] = {name: value}
            else:
                result["arguments"][name] = value

    return json.dumps(result)

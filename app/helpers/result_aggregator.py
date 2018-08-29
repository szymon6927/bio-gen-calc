def add_result(obj, name, value):
    if hasattr(obj, 'results'):
        name = name_converter(name)
        obj.results.append({'name': name, 'value': value})
    else:
        print(f'Object {obj} has no attr results', flush=True)


def name_converter(name):
    if name == "chi2_standard":
        return "Chi square"
    elif name == "chi_square":
        return "Chi square"
    elif name == "chi2_yats":
        return "Yate`s Chi square"
    elif name == "dof":
        return "dof"
    elif name == "p_standard":
        return "Chi square p-value"
    elif name == "p_yats":
        return "Yate`s Chi square p-value"
    elif name == "corelation_yats":
        return "Yate`s chi-square correlation"
    elif name == "corelation_standard":
        return "Chi-square correlation"
    else:
        return name


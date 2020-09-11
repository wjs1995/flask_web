def number_split(num):
    """
    12345678 => 12,345,678
    :param num:
    :return:
    """
    return '{:,}'.format(int(num))

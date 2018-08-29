import os
import uuid


def create_seq_file(content):
    """
    :param file name of file with sequences as content:
    :return:
    """
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'temp', str(uuid.uuid4()))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    tmpfile = open(filepath, "w+")
    filename = tmpfile.name
    tmpfile.write(content)
    tmpfile.close()

    return filename


def remove_temp_file(filename):
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'temp', filename)
    os.remove(filepath)

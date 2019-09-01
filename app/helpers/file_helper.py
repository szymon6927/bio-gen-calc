import os
import secrets
import uuid

from flask import current_app
from PIL import Image


def create_seq_file(content):
    """
    :param file name of file with sequences as content:
    :return:
    """
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'temp', str(uuid.uuid4()))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if type(content) is bytes:
        content = content.decode()

    tmpfile = open(filepath, "w+")
    filename = tmpfile.name
    tmpfile.write(content)
    tmpfile.close()

    return filename


def remove_temp_file(filename):
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'temp', filename)
    os.remove(filepath)


def allowed_file(filename):
    allowed_extension = set(['fasta', 'csv', 'xls'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads/profile_pics', picture_fn)

    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

from flask import send_file
import zipfile
from six import BytesIO

def send_build(filename, username, domain):
    with open(filename, 'rb') as f:
        zip_data = BytesIO(f.read())

    z = zipfile.ZipFile(zip_data, 'a')
    z.writestr('username.txt', str(username))
    z.writestr('ep.txt', str(domain))
    z.close()

    zip_data.seek(0)

    return send_file(
        BytesIO(zip_data.read()),
        attachment_filename="lockpick.zip",
        as_attachment=True
    )

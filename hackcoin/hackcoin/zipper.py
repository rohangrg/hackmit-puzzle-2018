import zipfile
from six import BytesIO
import io
import os
import glob

from hackcoin.config import DOMAIN
from flask import send_file

class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = BytesIO()

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of 
        file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0        

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        f = file(filename, "w")
        f.write(self.read())
        f.close()

def create_client_zip(username):
    directory = os.path.join('hackcoin', 'core')
    with open(os.path.join(directory, 'constants_template.py'), 'r') as f:
        constants_py = f.read() % (DOMAIN, username)
    
    z = InMemoryZip()
    z.append("constants.py", constants_py)

    for t in ("*.py", "*.md", "*.txt"):
        for fn in glob.glob(os.path.join(directory, t)):
            bn = os.path.basename(fn)
            
            # Ignore files.
            if bn in ('constants.py',
                      'constants_template.py',
                      'solve.py'):
                continue

            with open(fn, 'r') as f:
                z.append(bn, f.read())

    return send_file(
        io.BytesIO(z.read()),
        attachment_filename="client.zip",
        as_attachment=True
    )

if __name__ == "__main__":
    # Run a test.
    imz = InMemoryZip()
    imz.append("test.txt", "Another test").append("test2.txt", "Still another")
    imz.writetofile("test.zip")

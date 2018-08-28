import hashlib
import struct
SECRET = 'shhh'

with open('answers.txt', 'r') as f:
    answers = f.readlines()
    answers = [x.strip() for x in answers]

# Converts username to 0-255
def user_to_byte(u):
    m = hashlib.sha256((SECRET + u).encode('utf-8'))
    d = m.digest()
    i = struct.unpack('<B', d[0:1])[0]
    return i

def user_to_answer(u):
    i = user_to_byte(u) % len(answers)
    return answers[i]

def answer_to_file(answer):
    return hashlib.sha256((SECRET + answer).encode('utf-8')).hexdigest() + '.mp4'

def user_to_file(u):
    return answer_to_file(user_to_answer(u))

if __name__ == '__main__':
    # Spit out answers and their file names
    for answer in answers:
        print(answer, answer_to_file(answer))

import random
import string
import sys

def generate_dataset(size):
    used_words = set()
    while len(used_words) < size:
        length = random.randint(4, 20)
        used_words.add(random_string(length))
    dump_to_file(used_words, size)

def random_string(length):
    charset = string.ascii_letters + string.digits
    return ''.join(random.choice(charset) for x in range(length))

def dump_to_file(words, size):
    with open("data.csv", 'w') as f:
        f.write(str(size) + '\n')
        for word in words:
            just_size, just_char = get_additional_data(word)
            f.write(','.join([word, just_size, just_char]) + '\n')

def get_additional_data(word):
    length = len(word)
    justed_size = length + random.randint(0, 20)
    return str(justed_size), random_string(1)

if __name__ == "__main__":
    size = int(sys.argv[1])
    generate_dataset(size)
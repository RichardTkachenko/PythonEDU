import random, sys, time

SPEED = 0.01
LINE_PAUSE = 1.5


def slowPrint(text, pauseAmount=0.1):
    for character in text:
        print(character, flush=True, end='')
        time.sleep(pauseAmount)
    print()


print('niNety-nniinE BoOttels, by Al Sweigart al@inventwithpython.com')
print()
print('(Press Ctrl-C to quit.)')

time.sleep(2)

bottles = 99

lines = [' bottles of milk on the wall,',
         ' bottles of milk,',
         'Take one down, pass it around,',
         ' bottles of milk on the wall!']

try:
    while bottles > 0:
        slowPrint(str(bottles) + lines[0], SPEED)
        time.sleep(LINE_PAUSE)
        slowPrint(str(bottles) + lines[1], SPEED)
        time.sleep(LINE_PAUSE)
        slowPrint(lines[2], SPEED)
        time.sleep(LINE_PAUSE)
        bottles = bottles - 1

        if bottles > 0:
            slowPrint(str(bottles) + lines[3], SPEED)
        else:
            slowPrint('No more bottles of milk on the wall!', SPEED)

        time.sleep(LINE_PAUSE)
        print()

        lineNum = random.randint(0, 3)

        line = list(lines[lineNum])

        effect = random.randint(0, 3)
        if effect == 0:
            charIndex = random.randint(0, len(line) - 1)
            line[charIndex] = ' '
        elif effect == 1:
            charIndex = random.randint(0, len(line) - 1)
            if line[charIndex].isupper():
                line[charIndex] = line[charIndex].lower()
            elif line[charIndex].islower():
                line[charIndex] = line[charIndex].upper()
        elif effect == 2:
            charIndex = random.randint(0, len(line) - 2)
            firstChar = line[charIndex]
            secondChar = line[charIndex + 1]
            line[charIndex] = secondChar
            line[charIndex + 1] = firstChar
        elif effect == 3:
            charIndex = random.randint(0, len(line) - 2)
            line.insert(charIndex, line[charIndex])

        lines[lineNum] = ''.join(line)
except KeyboardInterrupt:
    sys.exit()

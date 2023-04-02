import json
import sys
import curses
import time

end_of_input = ['\n', '\t', ' ']

class Test():
    def __init__(self, count_word_in_text=0, count_error=0, speed=0, time_test=0):
        self.count_word_in_text = count_word_in_text
        self.count_error = count_error
        self.speed = speed
        self.time_test = time_test

    def __str__(self):
        return str(self.count_word_in_text) + ' ' + str(self.count_error) + ' ' + str(self.speed) + ' ' + str(self.time_test)

    def getList(self):
        return [count_word_in_text, count_error, speed]

current_tests = []

class DadaProcessor():
    @staticmethod
    def uploadCountOfTest():
        with open("data.json", 'r') as file:
            all_data = json.load(file)
            count_of_test = all_data['count of elements']
        return count_of_test

    @staticmethod
    def loadAllTest():
        with open("data.json", 'r') as file:
            all_data = json.load(file)
            all_test = all_data["data of tests"]
        return all_test

    @staticmethod
    def uploudTests():
        count_of_test = DadaProcessor.uploadCountOfTest()
        all_test = DadaProcessor.loadAllTest()

        all_test += current_tests
        count_of_test += len(current_tests)

        with open("data.json", 'r') as file:
            all_data = json.load(file)

        all_data["data of tests"] = all_test
        all_data["count of elements"] = count_of_test
            
        with open("data.json", 'w') as file:
            json.dump(all_data, file, indent=2)
                        
    @staticmethod
    def saveName(name):
        with open("config.json", 'r') as file:
            all_config = json.load(file)

        all_config['name'] = name

        with open("config.json", 'w') as file:
            json.dump(all_config, file, indent=2)

    @staticmethod
    def getName():
        with open("config.json", 'r') as file:
            all_config = json.load(file)
            name = all_config['name']
        return name

class Console():
    def __init__(self):
        self.stdsrc = curses.initscr()
        self.number_str = 0
        self.index_in_str = 0
        self.stdsrc.clear()

    def transportToNextLine(self):
        self.number_str += 1
        self.index_in_str = 0

    def sendMessage(self, message):
        self.stdsrc.addstr(self.number_str, self.index_in_str, message)
        temp = self.index_in_str + len(message)
        self.index_in_str = temp % curses.COLS
        self.number_str += temp // curses.COLS
        self.stdsrc.refresh()
        if message[-1] == '\n':
            self.transportToNextLine()

    def getChar(self):
        return self.stdsrc.getkey()
    
    def getMessage(self, is_blind=True):
        message = ''
        while True:
            key = self.getChar()
            if not is_blind:
                self.sendMessage(key)
            message += key
            if key in end_of_input:
                break
        return message

console = Console()

def start(stdsrc):
    name = DadaProcessor.getName()
    if name == '':
        name = initialize(console)
    DadaProcessor.saveName(name)
    console.sendMessage('hello ' + name)

def initialize(stdsrc):
    console.sendMessage("enter your name")
    console.transportToNextLine()
    return console.getMessage(is_blind=False)

def generateText():
    return "text for test"

def test(stdsrc):
    text = generateText()
    num_in_text = 0
    count_error = 0
    speed = 0
    console.sendMessage(text)
    console.transportToNextLine()

    start = time.time()

    while num_in_text < len(text):
        char = console.getChar()
        if char != text[num_in_text]:
            count_error += 1
        else:
            console.sendMessage(char)
            num_in_text += 1

    end = time.time()
    time_test = end - start
    console.transportToNextLine()
    count_word_in_text = len(text.split())
    console.sendMessage(f"your spped: {int(count_word_in_text / time_test * 60)} your error {count_error}")
    console.transportToNextLine()

    current_tests.append(str(Test(count_word_in_text=count_word_in_text,
                              count_error=count_error,
                              speed=speed,
                              time_test=time_test)))

def end(stdsrc):
   DadaProcessor.uploudTests()

def main():
    #curses.wrapper(TestConsole)
    curses.wrapper(start)
    for i in range(1):
        curses.wrapper(test)
    curses.wrapper(end)


if __name__ == "__main__":
    main()

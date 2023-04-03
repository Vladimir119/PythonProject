import json
import sys
import curses
import time
import matplotlib.pyplot as plt
import random

end_of_input = ["\n", "\t"]

class Test():
    def __init__(self, count_word_in_text=0, count_error=0, speed=0, time_test=0):
        self.count_word_in_text = count_word_in_text
        self.count_error = count_error
        self.speed = speed
        self.time_test = time_test

    def __str__(self):
        return str(self.count_word_in_text) + " " + str(self.count_error) + " " + str(self.speed) + " " + str(self.time_test)

    def getList(self):
        return [count_word_in_text, count_error, speed]

current_tests = []

class DadaProcessor():
    @staticmethod
    def getAllData(name_of_file):
        with open(name_of_file, "r") as file:
            all_data = json.load(file)
        return all_data

    @staticmethod
    def setAllData(name_of_file, all_data):
        with open(name_of_file, "w") as file:
            json.dump(all_data, file, indent=2)
    
    @staticmethod
    def uploadCountOfTest():
        all_data = DadaProcessor.getAllData("source/data.json")
        count_of_test = all_data["count of elements"]
        return count_of_test

    @staticmethod
    def loadAllTest():
        all_data = DadaProcessor.getAllData("source/data.json")
        all_test = all_data["data of tests"]
        return all_test

    @staticmethod
    def uploudTests():
        count_of_test = DadaProcessor.uploadCountOfTest()
        all_test = DadaProcessor.loadAllTest()
        
        global current_tests

        all_test += current_tests
        count_of_test += len(current_tests)

        all_data = DadaProcessor.getAllData("source/data.json")

        all_data["data of tests"] = all_test
        all_data["count of elements"] = count_of_test
            
        DadaProcessor.setAllData("source/data.json" ,all_data)
        current_tests = []

    @staticmethod
    def saveName(name):
        all_config = DadaProcessor.getAllData("source/config.json")

        all_config["name"] = name

        DadaProcessor.setAllData("source/config.json", all_config)

    @staticmethod
    def getName():
        all_config = DadaProcessor.getAllData("source/config.json")
        name = all_config["name"]
        return name

    @staticmethod
    def getAllSentenses():
        all_sentenses = []
        with open("source/sentenses.txt") as file:
            for line in file:
                line = line[:-1]
                all_sentenses.append(line)
        return all_sentenses

class Console():
    def __init__(self):
        self.stdsrc = curses.initscr()

        self.number_str = 0
        self.index_in_str = 0
        self.stdsrc.clear()

    def transportToNextLine(self):
        self.number_str += 1
        self.index_in_str = 0

    def sendMessage(self, message, color, without_move=False):
        self.stdsrc.addstr(self.number_str, self.index_in_str, message, color)
        if not without_move:
            temp = self.index_in_str + len(message)
            self.index_in_str = temp % curses.COLS
            self.number_str += temp // curses.COLS
            self.stdsrc.refresh()
            if len(message) >= 1 and message[-1] == "\n":
                self.transportToNextLine()

    def getChar(self):
        return self.stdsrc.getkey()
    
    def getMessage(self, is_blind=True):
        start_srt = self.number_str
        start_index_in_srt = self.index_in_str
        message = ""
        while True:
            key = self.getChar()

            if key == "KEY_BACKSPACE":
                if self.index_in_str != start_index_in_srt or self.number_str != start_srt:
                    if self.index_in_str == 0:
                        self.number_str -= 1
                        self.index_in_str = curses.COLS - 1;
                    else:
                        self.index_in_str -= 1
                    self.stdsrc.addstr(self.number_str, self.index_in_str, " ")
                    message = message[:-1]
                continue
            else:
                if not is_blind:
                    self.sendMessage(key, curses.color_pair(1))
                message += key
            if key in end_of_input:
                break
        return message

    def clear(self):
        self.stdsrc.clear()
        self.stdsrc.refresh()
        self.number_str = 0
        self.index_in_str = 0
        
all_sentenses = []
console = Console()

def start(stdsrc):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    name = DadaProcessor.getName()
    if name == "":
        name = initialize()
    DadaProcessor.saveName(name)
    console.sendMessage("hello " + name, curses.color_pair(1))
    global all_sentenses
    all_sentenses = DadaProcessor.getAllSentenses()

def initialize():
    console.sendMessage("enter your name", curses.color_pair(1))
    console.transportToNextLine()
    return console.getMessage(is_blind=False)

def generateText():
    count_of_sentenses = random.randint(1, 2)
    ans = ""
    for i in range(count_of_sentenses):
        diaposon = len(all_sentenses)
        num = random.randint(0, diaposon)
        ans += all_sentenses[num]
        if i != (count_of_sentenses - 1):
            ans += " "
    return ans

def test():
    text = generateText()
    num_in_text = 0
    count_error = 0
    speed = 0
    console.sendMessage(text, color=curses.color_pair(2), without_move=True)
    #console.transportToNextLine()

    is_start = False
    while num_in_text < len(text):
        char = console.getChar()

        if not is_start:
            start = time.time()
            is_start = True

        if char != text[num_in_text]:
            count_error += 1
        else:
            console.sendMessage(char,color=curses.color_pair(3))
            num_in_text += 1

    end = time.time()
    time_test = end - start
    console.transportToNextLine()
    count_word_in_text = len(text.split())
    speed = int(count_word_in_text / time_test * 60)

    console.sendMessage(f"your spped: {speed} your error {count_error}", curses.color_pair(2))
    console.transportToNextLine()

    current_tests.append(str(Test(count_word_in_text=count_word_in_text,
                              count_error=count_error,
                              speed=speed,
                              time_test=time_test)))

def buildGrafic():
    DadaProcessor.uploudTests()
    all_test = DadaProcessor.loadAllTest()
    x = []
    y_speed = []
    y_error = []
    counter = 1
    for test in all_test:
        x.append(counter)
        y_speed.append(int(test.split()[2]))
        y_error.append(int(test.split()[1]))
        counter += 1
    plt.plot(x, y_speed, label="speed", color="blue")
    plt.plot(x, y_error, label="error", color="red", linestyle="dashed")
    plt.xlabel("attempt")
    plt.ylabel("speed")
    plt.title("WPM grafic")
    plt.show()

def printHelp():
    console.sendMessage("""    commands:
    start test
    build grafic
    exit""", curses. color_pair(1))
    for i in range(4):
        console.transportToNextLine()
 

def end(stdsrc):
   DadaProcessor.uploudTests()

def work(stdsrc):
    while True:
        printHelp()
        message = console.getMessage(is_blind=False)
        message = message.strip()
        console.transportToNextLine()
        console.sendMessage(message, curses.color_pair(1))
        console.clear()
        if message == "exit":
            break
        if message == "build grafic":
            buildGrafic()
        if message == "start test":
            test()
        else:
            console.sendMessage("not command " + message, curses.color_pair(1))
            console.transportToNextLine()

def main():
    #start()
    #work()
    #end()
    curses.wrapper(start)
    curses.wrapper(work)
    curses.wrapper(end)

if __name__ == "__main__":
    main()

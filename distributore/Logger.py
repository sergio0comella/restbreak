class Logger:
    def info(*messages):
        string = ''
        for i in messages:
            string += str(i) + " "
        print('---', string, '---')

    def debug(*messages):
        return
        Logger.info(*messages)
        pass

    def goalReached():
        print("      ____             _     \n" +
              "     / ___| ___   __ _| |    \n" +
              "----| |  _ / _ \ / _` | |----\n" +
              "    | |_| | (_) | (_| | |    \n" +
              "     \____|\___/ \__,_|_|    \n")
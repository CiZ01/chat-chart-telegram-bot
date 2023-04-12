import chatminer.chatparsers as chatparsers
import chatminer.visualizations as vis
import matplotlib.pyplot as plt
import json


DEFUALT_STOPWORDS_JSON_PATH = 'service/api/utils_files/default_stopwords.json'

CMAP = {'Accent', 'Blues', 'BrBG', 'BuGn', 'BuPu', 'CMRmap', 'Dark2', 'GnBu', 'Greens', 'Greys', 'OrRd', 'Oranges', 'PRGn', 'Paired', 'Pastel1', 'Pastel2', 'PiYG', 'PuBu',
        'PuBuGn', 'PuOr', 'PuRd', 'Purples', 'RdBu', 'RdGy', 'RdPu', 'RdYlBu', 'RdYlGn', 'Reds', 'Set1', 'Set2', 'Set3', 'Spectral', 'Wistia', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'}

HELP_LINK = {'whatsapp': 'https://faq.whatsapp.com/1180414079177245/', 'instagram': 'https://help.instagram.com/181231772500920',
             'facebook': 'https://www.facebook.com/help/messenger-app/713635396288741', 'telegram': 'https://telegram.org/blog/export-and-more', 'signal': 'https://github.com/carderne/signal-export'}


class ChatMiner:

    userid = None
    df = None
    plots = []
    parser = None
    lang = None

    def __init__(self, parserName: str, filePath: str, userid: str, lang: str):
        '''
        Initialize the chat miner
        :param parserName: Name of the parser to use
        :param filePath: Path to the file to parse
        '''
        self.__choose_parser(parserName, filePath)

        # Parse the file
        self.parser.parse_file()
        self.df = self.parser.parsed_messages.get_df()

        # Set the userid
        self.userid = userid

        # Set the language
        self.lang = lang
        return

    def get_heatmap(self, years: tuple):
        '''
        Get the heatmap for the given dataframe
        :param df: The dataframe to use
        :return: The heatmap
        '''
        fig, ax = plt.subplots(len(years), 1, figsize=(9, int(len(years)*1.5)))

        try:
            for i in range(len(years)):
                ax[i] = vis.calendar_heatmap(
                    self.df, year=years[i], cmap=CMAP.pop(), ax=ax[i])
        except Exception as e:
            print("Error while plotting heatmap")
            print(str(e))
            return

        # Add to plots list
        self.plots.append(fig)
        return

    def get_wordcloud(self):
        '''
        Get the wordcloud for the given dataframe
        :param df: The dataframe to use
        :return: The wordcloud
        '''

        # Get stopwords
        stopwords = self.__get_stopwords()

        fig, ax = plt.subplots(1, 1, figsize=(9, 9))
        kwargs = {"background_color": "white",
                  "width": 800, "height": 300, "max_words": 500}
        ax = vis.wordcloud(self.df, stopwords=stopwords, ax=ax, **kwargs)
        self.plots.append(fig)
        plt.show()
        return

    def __choose_parser(self, parserName: str, filePath: str):
        '''
        Choose the parser to use
        :param parserName: Name of the parser to use
        :param filePath: Path to the file to parse
        :return: The parser to use
        '''
        # Choose parser
        # WHATSAPP PARSER
        if parserName == "WhatsAppParser":
            self.parser = chatparsers.WhatsAppParser(filePath)
        # TELEGRAM PARSER
        elif parserName == "TelegramJsonParser":
            self.parser = chatparsers.TelegramJsonParser(filePath)
        # FACEBOOK PARSER
        elif parserName == "FacebookMessengerParser":
            self.parser = chatparsers.FacebookMessengerParser(filePath)
        # INSTAGRAM PARSER
        elif parserName == "InstagramJsonParser":
            self.parser = chatparsers.InstagramJsonParser(filePath)
        return

    def __get_stopwords(self):
        '''
        Get the stopwords for the given language
        :return: The stopwords
        '''
        stopwords = {}
        with open(DEFUALT_STOPWORDS_JSON_PATH, 'r') as json_file:
            data = json.load(json_file)[self.lang]
            stopwords = set(item for sublist in data.values()
                            for item in sublist)
        return stopwords


if __name__ == "__main__":
    cm = ChatMiner("WhatsAppParser", "./_chat.txt", "1234", "it")
    cm.get_wordcloud()
    pass

import sys


class ConsolePrintFunctions:

    frames_collaction = {
        'default x': {'TR': '╳', 'TL': '╳', 'BR': '╳', 'BL': '╳', 'HO': '╳', 'VE': '╳'},
        'double square': {'TR': '╔', 'TL': '╗', 'BR': '╚', 'BL': '╝', 'HO': '═', 'VE': '║'},
        'single round': {"TR": "╭", "TL": "╮", "BR": "╰", "BL": "╯", "HO": "─", "VE": "│"},
        'single heavy square': {"TR": "┏", "TL": "┓", "BR": "┗", "BL": "┛", "HO": "━", "VE": "┃"},
        'single light square': {"TR": "┌", "TL": "┐", "BR": "└", "BL": "┘", "HO": "─", "VE": "│"},
        'double dash light': {"TR": "┌", "TL": "┐", "BR": "└", "BL": "┘", "HO": "╌", "VE": "╎"},
        'double dash heavy': {"TR": "┏", "TL": "┓", "BR": "┗", "BL": "┛", "HO": "╍", "VE": "╏"}
    }


    def print_one_line_title(self, text, frame_name):
        # fix illegal frame name
        if frame_name not in self.frames_collaction:
            frame_name = 'default x'
        frame = self.frames_collaction[frame_name]
        lines_add = ''
        for i in text:
            lines_add = lines_add + frame['HO']

        print(frame['TR'] + frame['HO'] + lines_add + frame['HO'] + frame['TL'])
        print(frame['VE'] + ' ' + text + ' ' + frame['VE'])
        print(frame['BR'] + frame['HO'] + lines_add + frame['HO'] + frame['BL'])

    def test_all_frames(self, text):
        for frame in self.frames_collaction:
            self.print_one_line_title(text, frame)

    def print_replaceable_line(self, text):
        return sys.stdout.write('\r' + text)

    text_index_sepatator = ' ➔ '

    def select_by_index(self, titles_list, print_before_input=None):

        if print_before_input is not None:
            print(print_before_input)

        loop_index = 0
        for title in titles_list:
            print(loop_index, self.text_index_sepatator, title)
            loop_index += 1
        return input()


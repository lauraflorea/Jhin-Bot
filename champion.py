class Champion:
    def __init__(self, name="", roles=(), rank=0, win_rate=(), pick_rate=()):
        self.__name = name
        self.__roles = roles
        self.__rank = rank
        self.__win_rate = win_rate
        self.__pick_rate = pick_rate

        alpha_name = filter(str.isalnum, name)
        self.__image = f'{"".join(alpha_name)}.png'

    def __repr__(self):
        return f'{self.get_name()} Object'

    def get_name(self):
        return self.__name

    def get_roles(self):
        return self.__roles

    def get_rank(self):
        return self.__rank

    def get_win_rate(self):
        return self.__win_rate

    def get_pick_rate(self):
        return self.__pick_rate

    def get_image_name(self):
        return self.__image

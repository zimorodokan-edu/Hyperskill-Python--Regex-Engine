def check_string(reg_string, text_string, begin=False, start_reg_string='', start_text_string='', symbol=''):
    # print(
    #     f'{symbol} reg_string={reg_string},
    #     text_string={text_string}, begin={begin},
    #     start_reg_string={start_reg_string},
    #     start_text_string={start_text_string}'
    #     )
    if start_reg_string == '':
        start_reg_string = reg_string
    if start_text_string == '':
        start_text_string = text_string
    reg = reg_string
    txt = text_string
    symbol = symbol

    def check_char(c1, c2):
        if c1 == '.' or c1 == c2:
            return True
        else:
            return False

    def check_special_char(c1, c2):
        if c1 == c2:
            return True
        else:
            return False

    if reg == '':
        return True

    if reg.startswith('^'):
        begin = True
        return check_string(reg[1:], txt, begin, start_reg_string, start_text_string, symbol='^')

    if txt == '':
        chars = ['?', '*']
        if reg.startswith(r'\\?'):
            return check_string(reg[3:], txt, begin, start_reg_string, start_text_string, symbol=symbol + ' ' + r'\\?')
        if reg.startswith(r'\\*'):
            return check_string(reg[3:], txt, begin, start_reg_string, start_text_string, symbol=symbol + ' ' + r'\\*')
        if len(reg) > 1 and not reg.startswith('\\') and reg[1] in chars:
            return check_string(reg[2:], txt, begin, start_reg_string, start_text_string, symbol)
        if reg[0] == '$':
            return True
        return False

    if len(reg) == 1:
        if reg[0] == '$':
            if len(txt) == 0:
                return True
            else:
                if begin is False:
                    return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string, symbol)
                else:
                    return False
        else:
            return check_char(reg[0], txt[0])

    if reg[0] != '\\':

        if reg[1] == '?':

            if check_string(reg[2:], txt, True, start_reg_string, start_text_string,
                            symbol=symbol + ' ' + reg[0] + '?0') is True:
                return True

            if check_char(reg[0], txt[0]):
                return check_string(reg[2:], txt[1:], True, start_reg_string, start_text_string,
                                    symbol=symbol + ' ' + reg[0] + '?')
            else:
                if begin is False:
                    return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                        symbol)
                else:
                    return False

        if reg[1] == '*':

            if check_string(reg[2:], txt, True, start_reg_string, start_text_string,
                            symbol=symbol + ' ' + reg[0] + '*0') is True:
                return True

            if check_char(reg[0], txt[0]):
                if check_string(reg[2:], txt[1:], True, start_reg_string, start_text_string,
                                symbol=symbol + ' ' + reg[0] + '*') is False:
                    return check_string(reg, txt[1:], True, start_reg_string, start_text_string, symbol)
                else:
                    return True
            else:
                if begin is False:
                    return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                        symbol)
                else:
                    return False

        if reg[1] == '+':
            if check_char(reg[0], txt[0]):
                if check_string(reg[2:], txt[1:], True, start_reg_string, start_text_string,
                                symbol=symbol + ' ' + reg[0] + '+') is False:
                    return check_string(reg, txt[1:], True, start_reg_string, start_text_string, symbol)
                else:
                    return True
            else:
                if begin is False:
                    return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                        symbol)
                else:
                    return False

        else:
            res = check_char(reg[0], txt[0])
            if begin is True:
                if res is True:
                    if len(txt) > 1:
                        return check_string(reg[1:], txt[1:], True, start_reg_string, start_text_string, symbol)
                    else:
                        return check_string(reg[1:], '', True, start_reg_string, start_text_string, symbol)
                else:
                    return False
            else:
                if res is True:
                    if len(txt) > 1:
                        return check_string(reg[1:], txt[1:], begin, start_reg_string, start_text_string, symbol)
                    else:
                        return check_string(reg[1:], '', begin, start_reg_string, start_text_string, symbol)
                else:
                    if len(txt) > 1:
                        return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                            symbol)
                    else:
                        return check_string(start_reg_string, '', begin, start_reg_string, start_text_string, symbol)

    elif reg.startswith(r'\\?'):
        print(r'startswith \\?')
        s = symbol + ' ' + r'\\?'

        if len(reg) > 3:
            if check_string(reg[3:], txt, True, start_reg_string, start_text_string,
                            symbol=s) is True:
                return True

            if txt.startswith(r'\\'):
                if len(txt) > 2:
                    return check_string(reg[3:], txt[2:], True, start_reg_string, start_text_string,
                                        symbol=s)
                else:
                    return check_string(reg[3:], '', True, start_reg_string, start_text_string,
                                        symbol=s)
            else:
                if begin is False:
                    return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                        symbol)
                else:
                    return False
        else:
            return True

    # elif reg.startswith(r'\\\\*'):
    # elif reg.startswith(r'\\\\+'):

    elif reg.startswith(r'\\'):
        print(r'startswith \\')
        symbol = symbol + ' ' + r'\\'

        if txt.startswith(r'\\'):
            if len(reg) > 2:
                if len(txt) > 2:
                    return check_string(reg[2:], txt[2:], True, start_reg_string, start_text_string,
                                        symbol=symbol)
                else:
                    return check_string(reg[2:], '', True, start_reg_string, start_text_string,
                                        symbol=symbol)
            else:
                return True

        else:
            if begin is False:
                if len(txt) > 2:
                    return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                        symbol=symbol)
                else:
                    return False
            else:
                return False

    else:
        res = None
        if reg.startswith(r'\?'):
            symbol = symbol + ' ' + r'\?'
            res = check_special_char('?', txt[0])
        elif reg.startswith(r'\*'):
            symbol = symbol + ' ' + r'\*'
            res = check_special_char('*', txt[0])
        elif reg.startswith(r'\+'):
            symbol = symbol + ' ' + r'\+'
            res = check_special_char('+', txt[0])
        elif reg.startswith(r'\.'):
            symbol = symbol + ' ' + r'\.'
            res = check_special_char('.', txt[0])
        elif reg.startswith(r'\$'):
            symbol = symbol + ' ' + r'\$'
            res = check_special_char('$', txt[0])

        if res is True:
            if len(reg) > 2:
                return check_string(reg[2:], txt[1:], True, start_reg_string, start_text_string, symbol=symbol)
            else:
                return True
        else:
            if begin is False:
                return check_string(start_reg_string, txt[1:], begin, start_reg_string, start_text_string,
                                    symbol=symbol)
            else:
                return False


reg, string = input().split('|')
reg = reg.replace(r'\\', '\\')
print(check_string(reg, string))

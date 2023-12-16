

def name_frame(message):
    border = '=' * (len(message) + 6)
    print('/' + border + '\\')
    print('| ' + message )
    print('\\' + border + '/')
    return

def message_frame(message):
    border = '=' * (len(message) + 4)
    print('==' + border + '==')
    print('|| ' + message + ' ||')
    print('==' + border + '==')

    return
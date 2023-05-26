from SessionMessage import sendSessionMessage

def otherOption():
    print('User selected Other Option')
    # Ask an Open ended Question
    openEndedQuestion = 'Write a crop you want to select'
    sendSessionMessage(openEndedQuestion)
    
import praw

class wComment:
    def __init__(self, seed):
        self.parent = str(seed.parent())
        self.id = seed.id
        self.author = str(seed.author)
        self.body = seed.body
        self.children = []
        for reply in seed.replies:
            self.children.append(wComment(reply))
    def display(self, outputFile):
        # print(self.author + ': ' + self.body + '\n--')
        outputFile.write(self.author + ': ' + self.body + '\n--\n')
        if len(self.children) > 0:
            for child in self.children:
                child.display(outputFile)
    
def main():
###
# Beginning message
###
    print("Beginning scrape...")

###
# Reddit Credentials
###
    reddit = praw.Reddit() #Fill this in with your own Reddit creds

###
# Get a list of submissions flaired as 'review' in a subreddit
###

    submissionList = []
    ###
    ### This reads from SubmissionList.txt, when a subreddit is previously scanned.
    ###
    with open('SubmissionList.txt') as f:
        for line in f:
            submissionList.append(reddit.submission(id=line))

    ###
    ### This scans a subreddit and creates SubmissionList.txt
    ###
    # PipeTobaccoReviews = reddit.subreddit('pipetobacco').submissions()
    # n = 1
    # for submission in PipeTobaccoReviews:
        # if submission.link_flair_css_class == 'Review':
            # submissionList.append(submission)
        # n += 1
        # if (n % 1000) == 0:
            # print('Scanned ' + str(n) + ' submissions.')


    # subFile = open('SubmissionList.txt', 'w')
    # for submission in submissionList:
        # subFile.write(str(submission.id) + '\n')
    # subFile.close()
    # submission = reddit.submission(id='828306') # Just a test review post

###
# The below code loops through each submission, outputting each submission to an individual text file with the self-text and every comment in the 
# correct message-response order (using fancy bs python recursive functions)
###
    n = 1
    for submission in submissionList:
        submission.comments.replace_more(limit=0)
        submissionTitle = str(submission.id) + '_' + str(submission.author) + '_' + submission.title[:20].replace('/','-')
        outputFileTitle = 'Reviews/' + submissionTitle.replace(' ', '_') + '.md'
        outputFile = open(outputFileTitle, 'w')
        outputFile.write(submission.title + '\nBy: ' + str(submission.author) + '\n---\n')
        outputFile.write(submission.selftext + '\n')
        commentdict = {}
        for comment in submission.comments:
            if str(comment.parent()) not in commentdict:
                commentdict[comment.id] = wComment(comment) 

        for ogID, ogMsg in commentdict.items():
            outputFile.write(36*'=' + '\n')
            ogMsg.display(outputFile)
        outputFile.close()
        n += 1
        if (n % 10) == 0:
            print('Wrote ' + str(n) + ' files.')

###
# Finished message
###
    print("Scrape complete.")

if __name__ == '__main__':
    main()

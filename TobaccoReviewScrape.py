###
 # PipeTobaccoReviewScrape.py
 # Z Wilder - 2018

 # MIT License

 # Copyright (c) 2018 Zach D Wilder

 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:

 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.

 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
###

import praw

###
# This class provides the recursion necessary to display comments in proper conversational order, as opposed to the BFS supplied by PRAW
###
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
#   PipeTobaccoReviews = reddit.subreddit('pipetobacco').submissions(1325376055,1522013635) # Added timestamp start/end information (thanks u/VilaFrancaWeimar for the idea!)
#   n = 1
#   for submission in PipeTobaccoReviews:
        ###
        ### These next three are just True/False shortcuts added for readability
        ###
#       containsReview = ('review' in submission.title) or ('Review' in submission.title) or ('REVIEW' in submission.title)
#       containsFirstImpressions = ('first impressions' in submission.title) or ('First Impressions' in submission.title) or ('First impressions' in submission.title)
#       reviewFlair = (submission.link_flair_css_class == 'Review')
#       if reviewFlair or containsReview or containsFirstImpressions:
#           submissionList.append(submission)
        ###
        ### Lines 86-88 Print something out every n % x submissions so that the user knows something is happening
        ###
#       n += 1
#       if (n % 100) == 0:
#           print('Scanned ' + str(n) + ' submissions.')


    ###
    ### 94-97 Write the scanned submissions to a file, this was originally added so I wouldn't have to wait forever to rescan submissions
    ###
#   subFile = open('SubmissionList_new.txt', 'w')
#   for submission in submissionList:
#       subFile.write(str(submission.id) + '\n')
#   subFile.close()

###
# The below code loops through each submission, outputting each submission to an individual text file with the self-text and every comment in the 
# correct message-response order (using fancy bs python recursive functions)
###
    n = 1
    for submission in submissionList:
        submission.comments.replace_more(limit=0)
        ###
        ### The submissionTitle is basically "SubmissionID_Author_First20OfTitle" - not ideal, but  since figuring out the blend requires human input
        ### figured this was the best way to go.
        ###
        submissionTitle = str(submission.id) + '_' + str(submission.author) + '_' + submission.title[:20].replace('/','-')
        
        ###
        ### 116-119 Write the file, then create the header and body of the file with the submission title, author, and self text.
        ### The selftext is needed for text submissions, since some reviews were done in the comments with a sweet picture in the post.
        ###
        outputFileTitle = 'Reviews/' + submissionTitle.replace(' ', '_') + '.txt'
        outputFile = open(outputFileTitle, 'w')
        outputFile.write(submission.title + '\nBy: ' + str(submission.author) + '\n---\n')
        outputFile.write(submission.selftext + '\n')

        ###
        ### 124-127 Gets the comments to print in a logical, question/response conversation order which required the hackery of the wComment class.
        ###
        commentdict = {}
        for comment in submission.comments:
            if str(comment.parent()) not in commentdict:
                commentdict[comment.id] = wComment(comment) 

        ###
        ### 132-135 Writes the comments to the file under the head and self text. The "36*'='" is a cheap way to make a nice spacer inbetween comments
        ###
        for ogID, ogMsg in commentdict.items():
            outputFile.write(36*'=' + '\n')
            ogMsg.display(outputFile)
        outputFile.close()

        n += 1
        if (n % 10) == 0:
            print('Wrote ' + str(n) + ' files.')

    print("Scrape complete.")

if __name__ == '__main__':
    main()

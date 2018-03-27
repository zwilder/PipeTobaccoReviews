# PipeTobaccoReviews

The impending doom of r/PipeTobacco led me to pretend I knew how to use python and write a simple script to scrape review data from the subreddit. This was
done mostly to help facilitate the migration of data from r/PipeTobacco to a new home, and was done without the consent of the moderators of that fine subreddit.
Hopefully, it helps someone out - there is a wealth of information there on these various blends, and would be a damn shame if it got spontaneously destroyed due
to enforcement of vague rules.

Contained within the 'ReviewsByBlend' folder is all 476 submissions to r/PipeTobacco that were flagged with the 'Review' flair along with their comments from the past
six years. The 'OtherReviews' folder contains various reviews of things that aren't tobacco (pipes, accessories, stores, etc).
The 'Reviews' folder has the latest scrape from r/PipeTobacco. __Last scrape done: 25March18 at 1433 AZ time (2133 GMT).__

Each file in the 'Reviews' folder is listed as the submission number, followed by the author name, followed by the first 20 characters of the review title. These
are then read and renamed appropriately as 'BlendName\_Author\_SubmissionID' and moved to the appropriate folder.

The SubmissionList.txt is a list of all ~~476~~ submission ID numbers, in case anyone wants them. TobaccoReviewScraper.py is the magic script, please excuse any
silliness in there or general bad programming - I have no idea what I'm doing (I call this style of programming 'Brute Force Python').

All work contained within each review is the original work of the respected author listed at the top of the file under the title. Please do not hesitate to 
contact me if I need to remove something.

_u/SickWillie_

---
TO DO:
* ~~Go through each individual submission and save in an alternate folder a new file with the filename as 'Tobacco Blend' + 'Author' +  'SubmissionID', since this would make everything much easier to actually view.~~ Done 26March18
* Remove any stray files in the submissions - I think theres a few in there that aren't really reviews but got auto-flagged as 'Reviews'. 
* Edit the search through the subreddit to look for the word 'review' in the title instead of looking for the flair. A much, much better way of going about this. (Thanks u/FuguSandwich!)
* Pull 'Good stuff' from the sidebar. It would stink to lose the 'If you like X, try Y' posts and the FAQ. (Thanks u/Heliumiami!)
* Include review date information - Not sure if this is actually useful, but maybe someone would want it. Should be a minor edit...

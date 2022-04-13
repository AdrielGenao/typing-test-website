from flask import Flask, request, render_template, redirect, session
from flask.helpers import url_for
import pandas as pd
import csv
import os
from profanity_filter import ProfanityFilter

app = Flask(__name__)
app.secret_key = os.urandom(16)

pf = ProfanityFilter()  # Profanity filter reader

tests=[  # List for tests to choose from
  "Today, historians relate that, as a general rule, buying and selling securities was very much unorganized before the year 1792. Every person who owned a security faced the problem of finding interested buyers who might consider the purchase of a debt-free investment. This meant most people were somewhat slow in investing in stocks and bonds because these securities could not readily be converted into money. We have been told that an interesting number of traders and merchants agreed to try to do something to help correct the situation.",
  "The fastest typing speed ever, 216 words per minute, was achieved by Stella Pajunas-Garnand from Chicago in 1946 in one minute on an IBM electric. As of 2005, writer Barbara Blackburn was the fastest English language typist in the world, according to The Guinness Book of World Records. Using the Dvorak Simplified Keyboard, she had maintained 150 wpm for 50 minutes, and 170 wpm for shorter periods, with a peak speed of 212 wpm. Blackburn, who failed her QWERTY typing class in high school, first encountered the Dvorak keyboard in 1938, quickly learned to achieve very high speeds, and occasionally toured giving speed-typing demonstrations during her secretarial career.",
  "The bikers rode down the long and narrow path to reach the city park. When they reached a good spot to rest, they began to look for signs of spring. The sun was bright, and a lot of bright red and blue blooms proved to all that warm spring days were the very best. Spring rides were planned. They had a burger at the lake and then rode farther up the mountain. As one rider started to get off his bike, he slipped and fell. One of the other bikers saw him fall but could do nothing to help him. Neither the boy nor the bike got hurt. After a brief stop, everyone was ready to go on. All the bikers enjoyed the nice view when they came to the top. All the roads far below them looked like ribbons.",
  "Frank Edward McGurrin, a court stenographer from Salt Lake City, Utah who taught typing classes, reportedly invented touch typing in 1888. On a standard keyboard for English speakers the home row keys are: \"ASDF\" for the left hand and \"JKL;\" for the right hand. The keyboard is called a QWERTY keyboard because these are the first six letters on the keyboard. Most modern computer keyboards have a raised dot or bar on the home keys for the index fingers to help touch typists maintain and rediscover the correct position on the keyboard quickly with no need to look at the keys.",
  "A writing sample is a supplemental document for a job application often requested for jobs that include a significant amount of writing, like those in journalism, marketing, public relations and research. Employers might also ask for a writing sample if you will be responsible for writing and communicating important information or correspondences. For example, if you are applying for a job in HR at a small company, you might be responsible for sending company-wide information. In this case, the employer will look for candidates with strong writing skills who can clearly communicate important information across the company.",
  "On July 16, 1969, the Apollo 11 spacecraft launched from the Kennedy Space Center in Florida. Its mission was to go where no human being had gone before—the moon! The crew consisted of Neil Armstrong, Michael Collins, and Buzz Aldrin. The spacecraft landed on the moon in the Sea of Tranquility, a basaltic flood plain, on July 20, 1969. The moonwalk took place the following day. On July 21, 1969, at precisely 10:56 EDT, Commander Neil Armstrong emerged from the Lunar Module and took his famous first step onto the moon\'s surface. He declared, \"That\'s one small step for man, one giant leap for mankind.\" It was a monumental moment in human history!",
  "Here is the perfect system for cleaning your room. First, move all of the items that do not have a proper place to the center of the room. Get rid of at least five things that you have not used within the last year. Take out all of the trash, and place all of the dirty dishes in the kitchen sink. Now find a location for each of the items you had placed in the center of the room. For any remaining items, see if you can squeeze them in under your bed or stuff them into the back of your closet. See, that was easy!",
  "The Blue Whales just played their first baseball game of the new season; I believe there is much to be excited about. Although they lost, it was against an excellent team that had won the championship last year. The Blue Whales fell behind early but showed excellent teamwork and came back to tie the game. The team had 15 hits and scored 8 runs. That\'s excellent! Unfortunately, they had 5 fielding errors, which kept the other team in the lead the entire game. The game ended with the umpire making a bad call, and if the call had gone the other way, the Blue Whales might have actually won the game.",
  "The school fair is right around the corner, and tickets have just gone on sale. We are selling a limited number of tickets at a discount, so move fast and get yours while they are still available. This is going to be an event you will not want to miss! First off, the school fair is a great value when compared with other forms of entertainment. Also, your ticket purchase will help our school, and when you help the school, it helps the entire community. But that\'s not all! Every ticket you purchase enters you in a drawing to win fabulous prizes. And don\'t forget, you will have mountains of fun because there are acres and acres of great rides, fun games, and entertaining attractions!",
  "Last week we installed a kitty door so that our cat could come and go as she pleases. Unfortunately, we ran into a problem. Our cat was afraid to use the kitty door. We tried pushing her through, and that caused her to be even more afraid. The kitty door was dark, and she couldn’t see what was on the other side. The first step we took in solving this problem was taping the kitty door open. After a couple of days, she was confidently coming and going through the open door. However, when we removed the tape and closed the door, once again, she would not go through. They say you catch more bees with honey, so we decided to use food as bait. We would sit next to the kitty door with a can of wet food and click the top of the can."
]

def getUsersInfo():  # Returns updated usersInfo array
    usersInfoDF=pd.read_csv(r"csvLocation.csv")  # Make Dataframe
    usersInfo=usersInfoDF[['Username','Password','Speed','Accuracy','Time Limit','Test']].sort_values(by="Speed",ascending=False).values  # Dataframe to numpy 2d array (w/o titles)
    usersInfo=usersInfo.tolist()    # This 2D array will be used for writing into the list
    return usersInfo

def getUsersLeaderboard():  # Returns updated usersLeaderboard array
    usersLeaderboardDF=pd.read_csv(r"csvLocation.csv")  # Make Dataframe
    usersLeaderboard=usersLeaderboardDF[['Username','Speed','Accuracy','Time Limit','Test']].sort_values(by="Speed",ascending=False).values  # Dataframe to numpy 2d array (w/o titles)
    usersLeaderboard=usersLeaderboard.tolist()  # This 2D array is used for sending to the html pages for displaying username and scores
    return usersLeaderboard

@app.route("/")  # Home page redirects to infinite page
def infiniteRedirect():
    return redirect(url_for("infinite",testNum=1))

@app.route("/<testNum>")  # Main route: infinite time limit page
def infinite(testNum):
    if(int(testNum)==len(tests)):  # Reset test list if testNum variable goes too far
        testNum=0
    return render_template("infinite.html",test=tests[int(testNum)],testnum=testNum)  # Rendering for full typing test page

@app.route("/60sec/<testNum>")  # 60 second time limit page
def sixtySec(testNum):
    if(int(testNum)==len(tests)):  # Reset test list if testNum variable goes too far
        testNum=0
    return render_template("60sec.html",test=tests[int(testNum)],testnum=testNum)  # Rendering for full typing test page

@app.route("/30sec/<testNum>")  # 30 second time limit page
def thirtySec(testNum):
    if(int(testNum)==len(tests)):  # Reset test list if testNum variable goes too far
        testNum=0
    return render_template("30sec.html",test=tests[int(testNum)],testnum=testNum)  # Rendering for full typing test page

@app.route("/signup/<testNum>")  # Signup page
def signup(testNum):
    return render_template("signup.html",testnum=testNum)  # Rendering singup page

@app.route("/login/<testNum>")  # Login page
def login(testNum):
    return render_template("login.html",testnum=testNum)  # Rendering login page

@app.route("/edit/<testNum>")  # Editing username page
def edit(testNum):
    if session.get('currentUser'):  # Checking if user is logged in by checking if currentUser exists
        return render_template("edit.html",testnum=testNum, username=session['currentUser'])
    return render_template("login.html",testnum=testNum)

@app.route("/editComplete", methods=["POST"])  # Editing new username given by user
def editComplete():
    usersInfo=getUsersInfo()  # Getting new usersInfo array
    newUsername=request.form["username"]  # Getting post information
    testNum=request.form["testnum"]
    for a in range(len(usersInfo)):
        if newUsername==usersInfo[a][0]:  # Checking if username already exists
            return render_template("editError.html", testnum=testNum,  username=session['currentUser'])  # Redirect to same signup page but with "username taken" at bottom
    usernameCopy=newUsername  # Copy of username to check for profane words
    usernameCopy=usernameCopy.replace(" ","")  # Deleting connecting characters and replacing numbers/special characters/numbers with correct letters for profanity check
    usernameCopy=usernameCopy.replace("-","")
    usernameCopy=usernameCopy.replace("+","")
    usernameCopy=usernameCopy.replace("_","")
    usernameCopy=usernameCopy.replace(".","")
    usernameCopy=usernameCopy.replace("*","")
    usernameCopy=usernameCopy.replace(",","")
    usernameCopy=usernameCopy.replace("/","")
    usernameCopy=usernameCopy.replace(":","")
    usernameCopy=usernameCopy.replace(";","")
    usernameCopy=usernameCopy.replace("'","")
    usernameCopy=usernameCopy.replace("\"","")
    usernameCopy=usernameCopy.replace("1","i")
    usernameCopy=usernameCopy.replace("!","i")
    usernameCopy=usernameCopy.replace("5","s")
    usernameCopy=usernameCopy.replace("$","s")
    usernameCopy=usernameCopy.replace("<","c")
    usernameCopy=usernameCopy.replace("4","a")
    if pf.is_profane(usernameCopy):
            return render_template("editProfanity.html", testnum=testNum, username=session['currentUser'])  # Redirect to same signup page but with "username taken" at bottom
    for a in range(len(usersInfo)):
        if session['currentUser']==usersInfo[a][0]:  # Looking for user
            usersInfo[a][0]=newUsername
    with open(r"csvLocation.csv", 'w') as csvfile:  # File as written mode
        csvwriter=csv.writer(csvfile)  # Create csv writing function
        usersInfo.insert(0,['Username','Password','Speed','Accuracy','Time Limit','Test'])  # Putting titles back in to rewrite csv file correctly
        rows=0
        while rows<len(usersInfo):
            csvwriter.writerow(usersInfo[rows])  # Rewrite 2d array back into file
            rows+=1
    session['currentUser']=newUsername  # Setting session currentUser to use for knowing which user is logged in
    return redirect(url_for("loggedInfinite",testNum=testNum))  # Redirect back to main page with new user information

@app.route("/signupComplete", methods=["POST"])  # Adding in new user, then redirects back to testing page but logged in
def signupComplete():
    usersInfo=getUsersInfo()  # Getting new usersInfo array
    username=request.form["username"]  # Getting post information
    password=request.form["password"]
    testNum=request.form["testnum"]
    for a in range(len(usersInfo)):
        if username==usersInfo[a][0]:  # Checking if user exists within system
            return render_template("signupError.html", testnum=testNum)  # Redirect to same signup page but with "username taken" at bottom
    usernameCopy=username  # Copy of username to check for profane words
    usernameCopy=usernameCopy.replace(" ","")  # Deleting connecting characters and replacing numbers/special characters/numbers with correct letters for profanity check
    usernameCopy=usernameCopy.replace("-","")
    usernameCopy=usernameCopy.replace("+","")
    usernameCopy=usernameCopy.replace("_","")
    usernameCopy=usernameCopy.replace(".","")
    usernameCopy=usernameCopy.replace("*","")
    usernameCopy=usernameCopy.replace(",","")
    usernameCopy=usernameCopy.replace("/","")
    usernameCopy=usernameCopy.replace(":","")
    usernameCopy=usernameCopy.replace(";","")
    usernameCopy=usernameCopy.replace("'","")
    usernameCopy=usernameCopy.replace("\"","")
    usernameCopy=usernameCopy.replace("1","i")
    usernameCopy=usernameCopy.replace("!","i")
    usernameCopy=usernameCopy.replace("5","s")
    usernameCopy=usernameCopy.replace("$","s")
    usernameCopy=usernameCopy.replace("<","c")
    usernameCopy=usernameCopy.replace("4","a")
    if pf.is_profane(usernameCopy):
            return render_template("signupProfanity.html", testnum=testNum)  # Redirect to same signup page but with "username taken" at bottom
    usersInfo.append([username,password,0,0,"",0])  # Appending new user to main list
    with open(r"csvLocation.csv", 'w') as csvfile:  # File as written mode
        csvwriter=csv.writer(csvfile)  # Create csv writing function
        usersInfo.insert(0,['Username','Password','Speed','Accuracy','Time Limit','Test'])  # Putting titles back in to rewrite csv file correctly
        rows=0
        while rows<len(usersInfo):
            csvwriter.writerow(usersInfo[rows])  # Rewrite 2d array back into file
            rows+=1
    session['currentUser']=username  # Setting session currentUser to use for knowing which user is logged in
    return redirect(url_for("loggedInfinite",testNum=testNum))  # Redirect back to main page with new user information

@app.route("/loginComplete", methods=["POST"])  # Route for making sure user exists
def loginComplete():
    usersInfo=getUsersInfo()  # Getting new usersInfo array
    username=request.form["username"]  # Getting post information
    password=request.form["password"]
    testNum=request.form["testnum"]
    for a in range(len(usersInfo)):
        if username==usersInfo[a][0] and password==usersInfo[a][1]:  # Checking if user exists within system
            session['currentUser']=username  # Setting session userIndex to use for knowing which user is logged in
            return redirect(url_for("loggedInfinite",testNum=testNum))  # Redirect back to main page with user now logged in
    return render_template("loginError.html", testnum=testNum)  # Redirect to same login page but with error at bottom

@app.route("/logout/<testNum>")  # Route for logging out of account
def logout(testNum):
    session.pop('currentUser', None)  # Popping current session variable
    return redirect(url_for("login",testNum=testNum))  # Redirect back to login page after clearing session variable

@app.route("/update/<testNum>", methods=["POST"])  # Route for updating new speed attained
def update(testNum):
    usersInfo=getUsersInfo()  # Getting new usersInfo array
    newSpeed=request.form["newSpeed"]  # Getting posted new Speed
    newAccuracy=request.form["newAccuracy"]  # Getting posted new Accuracy
    currentTime=request.form["currentTime"]  # Getting posted time setting used
    currentTest=request.form["currentTest"]  # Getting posted test typed
    for a in range(len(usersInfo)):  # Going through to find correct user and updating their new speed and accuracy, and updating which test and time limit used
        if session['currentUser']==usersInfo[a][0]:
            usersInfo[a][2]=int(newSpeed)
            usersInfo[a][3]=float(newAccuracy)
            usersInfo[a][4]=currentTime
            usersInfo[a][5]=int(currentTest)
    with open(r"csvLocation.csv", 'w') as csvfile:  # File as written mode
        csvwriter=csv.writer(csvfile)  # Create csv writing function
        usersInfo.insert(0,['Username','Password','Speed','Accuracy','Time Limit','Test'])  # Putting titles back in to rewrite csv file correctly
        rows=0
        while rows<len(usersInfo):
            csvwriter.writerow(usersInfo[rows])  # Rewrite 2d array back into file
            rows+=1
    return "done"

@app.route("/loggedInfinite/<testNum>")  # Infinite route with user logged in
def loggedInfinite(testNum):
    usersLeaderboard=getUsersLeaderboard()  # Getting new usersLeaderboard list
    if session.get('currentUser'):  # Checking if user is logged in by checking if currentUser exists
        if(int(testNum)==len(tests)):  # Reset test list if testNum variable goes too far
            testNum=0
        for a in range(len(usersLeaderboard)):  # Going through to find correct user
            if session['currentUser']==usersLeaderboard[a][0]:
                currentSpeed=usersLeaderboard[a][1]
        return render_template("loggedInfinite.html",test=tests[int(testNum)],testnum=testNum,users=usersLeaderboard,currentUser=session['currentUser'],currentSpeed=currentSpeed)  # Render Infinite page with user logged in
    return redirect(url_for("login",testNum=testNum))  # Redirect back to login page if currentUser variable does not exist

@app.route("/logged60sec/<testNum>")  # 60 second route with user logged in
def loggedSixtySec(testNum):
    usersLeaderboard=getUsersLeaderboard()  # Getting new usersLeaderboard list
    if session.get('currentUser'):  # Checking if user is logged in by checking if currentUser exists
        if(int(testNum)==len(tests)):  # Reset test list if testNum variable goes too far
            testNum=0
        for a in range(len(usersLeaderboard)):  # Going through to find correct user
            if session['currentUser']==usersLeaderboard[a][0]:
                currentSpeed=usersLeaderboard[a][1]
        return render_template("logged60sec.html",test=tests[int(testNum)],testnum=testNum,users=usersLeaderboard,currentUser=session['currentUser'],currentSpeed=currentSpeed)  # Render 60sec page with user logged in
    return redirect(url_for("login",testNum=testNum))  # Redirect back to login page if currentUser variable does not exist

@app.route("/logged30sec/<testNum>")  # 30 second route with user logged in
def loggedThirtySec(testNum):
    usersLeaderboard=getUsersLeaderboard()  # Getting new usersLeaderboard list
    if session.get('currentUser'):  # Checking if user is logged in by checking if currentUser exists
        if(int(testNum)==len(tests)):  # Reset test list if testNum variable goes too far
            testNum=0
        for a in range(len(usersLeaderboard)):  # Going through to find correct user
            if session['currentUser']==usersLeaderboard[a][0]:
                currentSpeed=usersLeaderboard[a][1]
        return render_template("logged30sec.html",test=tests[int(testNum)],testnum=testNum,users=usersLeaderboard,currentUser=session['currentUser'],currentSpeed=currentSpeed)  # Render 30sec page with user logged in
    return redirect(url_for("login",testNum=testNum))  # Redirect back to login page if currentUser variable does not exist

# Attendance-System
This project allows a faculty a get the names of absent students and those who have marked proxy.
The faculty needs to provide an attendance.txt file which the faculty may copy from the Chat Box of Google Meet, and a reference.csv file that the faculty can collect from the Admin office.

### Tech Stacks
1. HTML5 - To build the structure for webpages
2. Python 3.8 - Scripting Language for Backend
3. Flask - Micro Framework for Backend
4. Bootstrap-5 - CSS Framework to make responsive webpages

### Observations
The Names in Google Meet are maximum of three words long. Names longer than three words are omitted after the first three words.
For example:
The Name John Harry Rohan Doe will be displayed as John Harry Rohan.
The Names containing IITI do not have IITI in their Official Name List in reference.csv. Therefore, the word IITI is ignored in any Google Meet Name.
For example:
The name John IITI is officially listed as John in reference.csv 

### Assumptions
Two exactly similar names cannot be differentiated. This is because even Google Meet cannot differentiate between the two.
For students to mark their attendance, they must write their Roll Number (in the same format as in reference.csv) as the first word.
If these students do not write their correct Roll Number as the first word, they might not get marked as Present and may also be marked for putting Proxy Attendance for their fellow batchmate.

The students who have asked the Admin Office to change their names in Google Meet (For, eg. John Harry Rohan Doe asks Admin Office to keep his name as Harry Doe in Google Meet) must also ask the respective faculty to change their name in reference.csv.
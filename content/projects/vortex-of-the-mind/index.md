---
title: "Vortex of the Mind"
description: "Lorem ipsum dolor sit amet"
date: 1993-11-27T17:58:38-06:00
draft: false
type: "project"
---

```basic
100 REM ****************************** START
101 PRINT "THIS GAME IS LICENSED TO MRS. OLSON"
102 PRINT ""
101 PRINT "     Welcome, what is your name?"
102 INPUT "     ";a$
107 FOR i=1 TO 5
108 PRINT ""
109 NEXT i
103 PRINT "     Hello, ";a$; ", prepare to blow your mind in ..."
104 PRINT ""
104 PRINT ""
105 PRINT "                          ... Kyle's VORTEX OF THE MIND"
106 PRINT "                             ... Kyle's VORTEX OF THE MIND"
105 PRINT "                                ... Kyle's VORTEX OF THE MIND"
107 FOR i=1 TO 10
108 PRINT ""
109 NEXT i
112 INPUT "                                        ... press RETURN to continue";Q$
126 PRINT "......"
127 PRINT "You " ;a$;", have traveled to many far away lands and conquered many"
120 PRINT "foes.  But now you are about embark on an amazing journey, a"
121 PRINT "journey into KYLES VORTEX OF THE MIND."
122 PRINT ""
123 PRINT ""
124 PRINT ""
125 PRINT "On the way, you will face many decisions and challenges."
126 PRINT "But remember you must not let the evil subduct you for you are on"
127 PRINT "a misson of peace.  Your goal is to rescue the king from his own"
120 PRINT "split personality - your foe the hairy bloat!"
121 PRINT ""
122 INPUT "                                         ...Press RETURN to continue";d$
123 PRINT "(NOTE)"
124 PRINT "Certain rooms are only accessible through random teleportation."
125 PRINT ""
126 PRINT ""
127 PRINT "......"
138 INPUT "                                        ... press RETURN to continue   ";Q$
1000 REM ****************************** ENTRY ROOM
1001 REM
1002 PRINT "You are in the ENTRY ROOM"
1003 PRINT ""
1004 PRINT "You are standing in a big room."
1005 PRINT "There is only one door which opens to the South."
1006 PRINT "Do you want to enter? (y/n)"
1007 PRINT ""
1008 INPUT b$
1009 IF b$="y" GOTO 2000
1010 PRINT "The ceiling slowly moves downward and crushes your skull."
1011 PRINT "You should have entered."
1012 GOTO 20000
2000 REM ****************************** GATEWAY ROOM
2001 REM
2002 PRINT "You are in the GATEWAY ROOM"
2003 PRINT ""
2004 PRINT "You are in a room with four doors."
2005 PRINT "The door to the East is locked."
2006 PRINT "The doors to the North, South, and West are wide open."
2007 PRINT "Where do you want to go (n/s/w/e)?"
2008 INPUT b$
2009 PRINT ''"
2011 IF b$="n" THEN 1000 REM ENTRY ROOM
2013 IF b$="s" THEN 4000 REM CHAMBER OF HORROR
2015 IF b$="w" THEN 3000 REM DIMENSIONAL WARP
2017 IF b$="e" THEN 2019 REM ASK FOR CODE
2018 GOTO 2007
2019 PRINT "Please enter the code"
2020 INPUT p$
2021 IF p$ <> "open door oh god of all that walks" THEN 2007
2022 PRINT ""
2023 PRINT "The door slowly starts to open almost like magic."
2024 PRINT "Do you enter ? (y/n)"
2025 INPUT f$
2026 IF f$ = "n" THEN 2000
2027 PRINT ''
2028 GOTO 11000 REM GARDEN OF STONE
3000 REM ****************************** DIMENSIONAL WARP
3001 REM
3002 PRINT "You are in the DIMENSIONAL WARP"
3003 PRINT ""
3004 PRINT "POOF !!"
3005 PRINT "You are gone."
3006 PRINT ''
3007 GOTO 900 REM UPSIDE DOWN ROOM
4000 REM ****************************** CHAMBER OF HORROR
4001 REM
4002 PRINT "You are in the CHAMBER OF HORROR"
4003 PRINT ""
4004 PRINT "A wraith appears out of nowhere and emits a
4005 PRINT "   blood curdling scream"
4006 PRINT "There are only three doors."
4007 PRINT "One is to the East and one to the north the other is to the West."
4008 PRINT ""
4009 PRINT "Which door do you choose? (e/w)"
4010 INPUT b$
4011 IF b$="e" THEN GOTO 5000 REM NO ROOM
4012 IF b$="w" THEN 6000 REM ROOM OF THE HAIRY BLOAT
4013 IF B$ = "n" THEN 2002 REM Gateway room
4014 GOTO 4009
5000 REM ****************************** NO ROOM
5001 REM
5002 PRINT "You are in the NO ROOM"
5003 PRINT ""
5004 PRINT "God, are you dumb 0!0!0!"
5005 PRINT "You are going forward."
5006 PRINT "You smack your head into the wall, boy that wasn't very smart."
5007 PRINT "You are going backward."
5008 PRINT "You smack your head into the wall, boy that wasnt very smart."
5009 PRINT ""
5010 GOTO 5005
6000 REM ****************************** ROOM OF THE HAIRY BLOAT
6001 REM
6002 PRINT "You are in the ROOM OF THE HAIRY BLOAT"
6003 PRINT ""
6004 PRINT "You are going West"
6005 PRINT "You cannot return this way."
6006 PRINT "You enter a room with a very fat man sitting in a very old chair."
6007 PRINT "You try to say hello to the man but he does not answer."
6008 PRINT "He only gives you the key to the East door"
6009 PRINT "   in the GATEWAY ROOM."
6010 PRINT "If you say the words 'open door oh god of all that walks'"
6011 PRINT "   it shall be done."
6012 PRINT "This room has three doors."
6013 PRINT "They go North, South and East."
6014 PRINT "Where do you want to go? (n/s/e)"
6015 INPUT b$
6016 IF b$="n" THEN 7000 REM ZOMBIE ROOM
6017 IF b$="w" THEN 8000 REM UPSIDE DOWN ROOM
6018 IF b$="s" THEN 9000 REM LIFE OR DEATH ROOM
6019 IF b$="e" THEN 4002 REM CHAMBER OF HORRER
6020 PRINT ''
6021 GOTO 6014
7000 REM ****************************** ZOMBIE ROOM
7001 REM
7002 PRINT "You are in the ZOMBIE ROOM"
7003 PRINT ""
7004 PRINT "There two doors, one to the East and one to the South"
7005 PRINT "Where do you want to go?  (e/s)?"
7006 PRINT "Wait!  A zombie starts at you and eats you."
7007 GOTO 20000
8000 REM ****************************** UPSIDE DOWN
8001 REM
8002 PRINT "You are in the UPSIDE DOWN"
8003 PRINT ""
8004 PRINT "As you turn to go left a trap door opens and you fall down a hole."
8005  PRINT "You don't understand the door that was just there is now gone."
8006 PRINT "Suddenly, you land with a thump."
8007 PRINT "You find yourself in a large room where everything is"
8008 PRINT "   upside down.
8009 PRINT "You feel weird.
8010 PRINT "There is one door to the East of you."
8011 PRINT "Do you want to enter? (y/n)"
8012 INPUT b$
8013 PRINT ""
8014 IF b$="y" THEN 7000 REM LIFE OR DEATH ROOM
8015 PRINT "The ground shakes, ";a$;".  You fall into a pit of bubbling"
8016 PRINT "   brains on acid."
8017 GOTO 20000
9000 REM ****************************** LIFE OR DEATH ROOM
9001 REM
9002 PRINT "You are in the LIFE OR DEATH ROOM"
9003 PRINT ""
9004 PRINT "Do you want to die? (y/n)"
9005 INPUT b$
9006 IF b$ = "n" THEN 9009
9007 IF b$ = "y" THEN 20000
9008 GOTO 9004
9009 PRINT "Suddenly you warp to the FIRE ROOM."
10000 REM ****************************** FIRE ROOM
10001 REM
10002 PRINT "You are in the FIRE ROOM"
10003 PRINT ""
10004 PRINT "You are in a large room with no exits."
10005 PRINT"Sudenly a fire beast starts you on fire you jump"
10006 PRINT "   into a pool of water."
10007 PRINT "You swim  until you end up in a  garden made of stone.
10008 PRINT "You stumble around in the darkness."
11000 REM ****************************** GARDEN OF STONE
11001 REM
11002 PRINT "You are in the GARDEN OF STONE"
11003 PRINT ""
11004 PRINT "You look around but your attempt is in vain for you can't see"
11005 PRINT "   because there is no light."
11006 PRINT "Do you want to look for a torch? (y/n)"
11007 INPUT q$
11008 IF q$ = "n" THEN 11012
11009  PRINT "You attempt to look for a torch but stumble and fall"
11010 PRINT "   causing you to break your neck."
11011 GOTO 20000
11012 PRINT "You decide not to look for a torch and after about a"
11013 PRINT "minute or so a trap door opens"
11014 PRINT "You see a pipe do you grab it? (y/n)"
11015 INPUT t$
11016 IF t$ = "y" THEN 11019
11017 PRINT "you decide not to grab the pipe and fall to your death."
11018 GOTO 20000
11019  PRINT "You grab the pipe and avoid falling to your death as you"
11020 PRINT "   climb out."
11021 PRINT " You remember never to stand there again."
11022 PRINT "When you get out of the trap the room is different."
11025 PRINT " the room is differant for it is made of glass there is a statue of"
11028 PRINT "the hairy bloat this is very odd"
11031 PRINT " do you want to take a closer look? (y/n)
11034 INPUT z$
11037 IF z$ = "n" THEN 11125
11040 PRINT "as you are takeing a closer look you loose your balance and grab"
11043 PRINT "the arm of the hairy bloat and from his cup an acid pours out"
11046 PRINT " you see that it is quickly refilled from a tube op his arm"
11049 PRINT " do you want to try to burn a door in the wall? (y/n)"
11052 INPUT m$
11052 IF m$ = "n" THEN 11125
11055 PRINT "you sucseed and with one drop of acid a door is made"
11058 PRINT "do you enter? (y/n)"
11061 INPUT t$
11062 IF t$ = "n" THEN 11125
11065 PRINT " the room is very dark then you hear the voice of the hairy bloat"
11069 PRINT "then he speaks THOU ART DAMNED FOR ENTERING THE VORTEX"
11071 PRINT " OF THE MIND"
11074 PRINT "then he points a hairy finger at you and zap"
11123 PRINT "You are teleported to a different room."
11124 GOTO 12000
11125 PRINT " you do nothing for the next 8 days and starve to death"
11126 GOTO 100
12000 REM ******************************RANDOM TELEPORT
12001 REM
12000 z=13*RND(1)+1
12001 z=INT(z)
12003 IF z=1 THEN 1000 REM ENTRY ROOM
12005 IF z=2 THEN 2000 REM GETWAY ROOM
12007 IF z=3 THEN 3000 REM DIMENSIONAL WARP
12009 IF z=4 THEN 4000 REM CHAMBER OF HORROR
12003 IF z=5 THEN 5000 REM NO ROOM
12005 IF z=6 THEN 6000 REM ROOM OF THE HAIRY BLOAT
12007 IF z=7 THEN 7000 REM ZOMBIE ROOM
12009 IF z=8 THEN 8000 REM UPSIDE DOWN ROOM
12003 IF z=9 THEN 9000 REM LIFE OR DEATH ROOM
12005 IF z=10 THEN 10000 REM FIRE ROOM
12007 IF z=11 THEN 11000 REM GARDEN OF STONE
12009 IF z=12 THEN 20000 REM RANDOM TELEPORT
12010 IF z= 13 THEN 20008 REM random teleport
20000 REM ****************************** RESTART
20001 REM
20002 PRINT "You are finished here."
20003 REM
20004 PRINT "Do you want to play again? (y/n)"
20005 INPUT r$
20006 IF r$="y" THEN 100
20007 IF r$="n" THEN STOP
20008 PRINT "you are transported to a room with nothing in it execpt"
20010 PRINT "a piece of moldy stinky spoiled meat"
20020 PRINT " you take the meat and put it in your pack"
20025 PRINT "there is a door to the east and south where do you go? (e/s)"
20030 INPUT j$
30035 IF j$= "e" THEN 30050
30040 PRINT "you are going south you enter a room where the only door is"
30045 PRINT "to the south"
```
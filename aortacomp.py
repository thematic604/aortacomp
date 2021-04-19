#!/usr/bin/python
import os,re,sys
"""Look at local Art of Rally records in Leaderboards.txt and find slow entries

So any time made in any group but the fastest, which is faster than the
corresponding time from any faster group gets added to the report.

Car numbers are counting from the default on, with 2 being the one you
get after changing the car one step in the game menu.

One (1) optional argument is used, for the location of this file.
"""

"""Give a hint of what to do if there's not enough
data
"""
def unsatis():
    print "Custom rallies in more than one group and on the same stages"
    print "is an easy way to make sure there's enough records to work with."
    quit

"""Read file into a list object.
"""
def makeblist(leadb):
    lblist = []
    for line in leadb:
        if any(x in line for x in ["Group","_60s","_70s","_80s"]):
            lblist.append(line)
    return(lblist)

"""Check starting argument to use as work directory.
"""
try:
    if len(sys.argv[1]) > 0:
        print sys.argv
        os.chdir(sys.argv[1])
except IndexError:
    pass

"""Open a file of records and read it into a list object.
"""
entries = {}
try:
    with open("Leaderboards.txt", "r") as lbfile:
        lblist = makeblist(lbfile)
#        lblist = []
#        for line in lbfile:
#            if any(x in line for x in ["Group","_60s","_70s","_80s"]):
#                lblist.append(line)
except IOError:
    with open("Save/Leaderboards.txt", "r") as lbfile:
        lblist = makeblist(lbfile)

"""Iterate over the created list and turn it into a dictionary
within a dictionary. The actual record is a tuple with the chosen car.
"""
for lbitem in lblist:
    esearch = re.search(r"(.*(Dry|Wet))_(.*):(\d*):([0-9])", lbitem)
    if esearch:
        foundpla = esearch.group(1)
#       foundgri = esearch.group(2)
        foundgrp = esearch.group(3)
        foundrec = esearch.group(4)
        foundveh = esearch.group(5)
        if len(foundgrp) >= 1:
            try:
                entries[foundgrp].update({foundpla:(foundrec,foundveh)})
            except KeyError:
                entries.update({foundgrp:{foundpla:(foundrec,foundveh)}})

"""Describe the groups previously found in "descending order
per speed". Complain if less than two are found.
"""
validcmp = []

print "Added",
gcollection = []
gcolstr = ''
greport = ''
try:
    if entries["GroupA"] != '':
        validcmp += ["GroupA"]
        gcollection += ["Group A"]
except KeyError: pass
try:
    if entries["GroupS"] != '':
        validcmp += ["GroupS"]
        gcollection += ["Group S"]
except KeyError: pass
try:
    if entries["GroupB"] != '':
        validcmp += ["GroupB"]
        gcollection += ["Group B"]
except KeyError: pass
try:
    if entries["80s"] != '':
        validcmp += ["80s"]
        gcollection += ["Group 4"]
except KeyError: pass
try:
    if entries["70s"] != '':
        validcmp += ["70s"]
        gcollection += ["Group 3"]
except KeyError: pass
try:
    if entries["60s"] != '':
        validcmp += ["60s"]
        gcollection += ["Group 2"]
except KeyError: pass

validcmpl = len(validcmp)
if len(validcmp) == 0:
    print "nothing."
    unsatis()
for gcomp in gcollection:
    gcolstr += gcomp+", "
validstr = str(validcmpl)
greport += gcolstr + "found " + validstr + " to compare."
print greport
if len(validcmp) < 2:
    print 
    print "Did not find two rally groups in here."
    unsatis()

"""Compare times across groups per stage.

If a faster group time is found to have a slower record,
highlight it. Compare to the slowest group first.
"""

hitcounter = 0
iy = 1
resultstr,ucar,lcar = "","",""

print "Looking for internally slow records..."
for vgrp in validcmp:
    if vgrp == validcmp[-1]:
        break
    for compx in entries[vgrp]:
# here should be prepared a loop to go through between max-1..1 groups
        for cgrp in reversed(validcmp[validcmp.index(vgrp):]):
            try:
                if float(entries[vgrp][compx][0]) > \
                float(entries[cgrp][compx][0]):
                    hitcounter += 1
                    stageneat = re.sub("_"," ",re.sub(r"Forward",r"(F)",compx))
                    rdiff = float(entries[vgrp][compx][0])/1000 - \
                    float(entries[cgrp][compx][0])/1000
                    vveh = entries[vgrp][compx][1]
                    cveh = entries[cgrp][compx][1]
                    if cveh == "0":
                        ucar = "default"
                    else:
                        ucar = "car "+str(int(cveh)+1)
                    if vveh == "0":
                        lcar = "default"
                    else:
                        lcar = "car "+str(int(vveh)+1)
                    resultstr += "Slow time: "
                    resultstr += "\n"+stageneat+", "
                    resultstr += str(gcollection\
                    [(validcmp.index(cgrp))])+" ("+ucar+") record is faster "
                    resultstr += "than "+str(gcollection\
                    [(validcmp.index(vgrp))])+\
                    " ("+lcar+") record.\nThe difference is "+str(rdiff)+\
                    " s.\n\n"
            except KeyError: pass

if hitcounter == 0:
    print "Found absolutely nothing!"
elif hitcounter >= 1:
    print resultstr
    print "That's",hitcounter,"cases you can work on."
else:
    print "Unknown error!"
    quit
    

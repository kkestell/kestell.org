---
title: "Test"
description: "Blah blah blah blah blah"
created: 2023-03-04
updated: 2023-03-04
---

Lorem ipsum dolor sit amet[^1].

```python
@decorator(param=1)
def f(x):
    """ Syntax Highlighting Demo
        @param x Parameter"""
    s = ("Test", 2+3, {'a': 'b'}, x)   # Comment
    print s[0].lower()
    for t in s:
        if t in s:
            print('sorry') 
            x & s


class Foo:
    def __init__(self):
        byte_string = 'newline:\n also newline:\x0a'
        text_string = u"Cyrillic Я is \u042f. Oops: \u042g"
        self.makeSense(whatever=1)

    def makeSense(self, whatever):
        self.sense = whatever
        if True:
            pass

x = len('abc')
print(f.__doc__)

# nested `in` operator
requested toppings = ['mushrooms', 'french fries', 'extra cheese']
for requested_topping in requested_toppings:
    if requested topping in available toppings:
        print (f'Sorry, we do not have {requested_topping)')
print('Infinished making your pizza!')
```

Lorem ipsum dolor[^2] sit amet.

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>

using namespace std;

void InitMap(map<string, vector<string> > &svmap, ifstream &ifile)
{
	string textline;
	while (getline(ifile, textline, '\n')) {
		string familyName;
		vector<string> child;
		string::size_type nowPos = 0, prevPos = 0, textSize = textline.size();
		if (!textSize)
			continue;
		while ((nowPos = textline.find_first_of(' ', nowPos)) != string::npos) {
			string::size_type endPos = nowPos - prevPos;
			if (!prevPos)
				familyName = textline.substr(prevPos, endPos);
			else
				child.push_back(textline.substr(prevPos, endPos));
			prevPos = ++nowPos;
		}
		if (prevPos < textSize)
			child.push_back(textline.substr(prevPos, nowPos - prevPos));
		if (!svmap.count(familyName))
			svmap[familyName] = child;
		else
			cerr << "Sorry, we already have a "<< familyName << " family in our map!\n";
	}
}

void DisplayMap(map<string, vector<string> > &svmap, ofstream &ofile)
{
	for (map<string, vector<string> >::iterator itr = svmap.begin(), mapEnd = svmap.end(); itr != mapEnd; ++itr) {
		ofile << "The " << itr->first << " family ";
		if (itr->second.empty())
			ofile << "has no children." << endl;
		else {
			ofile << "has " << itr->second.size() << " children: ";
			for (vector<string>::iterator itrvec = itr->second.begin(), vecEnd = itr->second.end(); itrvec != vecEnd; ++itrvec)
				ofile << *itrvec << " ";
			ofile << endl;
		}
	}
}

void UserQuery(map<string, vector<string> > &svmap)
{
	string queryName;
	cout << "Please enter a family name you want to query: ";
	cin >> queryName;
	int i = 0;
	for (map<string, vector<string> >::iterator itr = svmap.begin(), mapEnd = svmap.end(); itr != mapEnd; ++itr) {
		i++;
		if (itr->first == queryName) {
			cout << "The " << itr->first << " family has " << itr->second.size() << " children: ";
			for (vector<string>::iterator itrvec = itr->second.begin(), vecEnd = itr->second.end(); itrvec != vecEnd; ++itrvec)
				cout << *itrvec << " ";
			break;
		}
	}
	if (i >= svmap.size())
		cout << "Sorry, the " << queryName << " family is not found." << endl;
}

int main(int argc, char *argv[])
{
	ifstream readFile("TestFile_3.3.txt");
	ofstream writeFile("TestFile_3.3.map");
	if (!readFile.is_open() || !writeFile.is_open()) {
		cerr << "Sorry, the file fails to read!" << endl;
		return -1;
	}
	map<string, vector<string> > mapFamily;
	InitMap(mapFamily, readFile);
	DisplayMap(mapFamily, writeFile);
	UserQuery(mapFamily);
	return 0;
}
```

```shell
#!/bin/bash

# This script does nothing in particular
# It somehow manages to include most of Bash's syntax elements :)

# Computes the number 42 using Bash
function compute42() {
    echo $((2 * 3 * (3 + 4)))
}

# Computes the number 42 using a subshell command
function compute42Subshell() {
    echo "$(echo "2*3*(3+4)" | bc)"
}

# Subtract the second parameter from the first and outputs the result
# It can only handle integers
function subtract() {
    local a=${1:?"First param not set"}
    local b=${2:?"Second param not set"}

    echo -n "$((a - b))"
}

echo 'The current working directory is: '" ${PWD}"

echo "100 - 58 = $(subtract 100 58)"

fortyTwo=$(compute42)
echo "$fortyTwo is 42"

fortyTwo=$(compute42Subshell)
echo "${fortyTwo} is 42"

echo "6 * 7 is $fortyTwo"  > log.txt 2>&1

echo `echo This is an echo`

empty=""
[ -z "$empty" ]  && This variable is empty!

cat -  << EOF
    Dear Mr. X,
    this is a message to you.

    With kind regards,
    Mr. Y
EOF
```

[^1]: Blah blah footnote!

[^2]: Blah blah footnote! Blah blah footnote! Blah blah footnote! Blah blah footnote! Blah blah footnote! Blah blah footnote! Blah blah footnote! 
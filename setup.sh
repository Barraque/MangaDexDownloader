#!/bin/bash

while read line
do 
	python3 -m pip install $line --user
done < dependencies.txt

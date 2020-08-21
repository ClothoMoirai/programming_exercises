#!/bin/bash
# Assisting an acquaintance who needed a way to split each of many CSV files approximately in half.
# split -nl/2 could be used if all lines are the same length or approximation is okay as -n splits on the basis of byte size.
for i in *.csv; do
	csvlength=$(wc -l $i | cut -d' ' -f1)
	splitlength=$(( $csvlength - ($csvlength / 2)))
	split -l${splitlength} --numeric-suffixes=1 -a1 --additional-suffix=.csv $i $( echo $i | cut -d'.' -f1)
done

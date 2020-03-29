#!/bin/bash

TEMPLATE="./lpp.txt.template"
REPLACE_START_CHAR='<'
REPLACE_END_CHAR='>'
OUTPUT="./lpp.txt"
MIDI_C1_NOTE=36
GRID=8


OVERLAP=0
TRANSPOSE=2


COLOR_OUTPUT="lpp-colors.smidi"
SYSEX_HEADER='0 32 41 2 16 15 1'
NUM_NOTES_OCTAVE=22
COLORS=('25  25  25'
'30  2   2'
'0   0   0'
'0   0   0'
'0   10  0'
'5   5   63'
'0   0   0'
'0   0   0'
'0   80  80'
'24  8   0'
'0   0   0'
'0   0   0'
'15  2   0'
'33  20  0'
'70  0   40'
'0   0   0'
'0   0   0'
'18  9   20'
'30  10  10'
'0   0   0'
'0   0   0'
'80  0   10')



echo "" > "${OUTPUT}"
echo 'dev "Launchpad Pro Standalone Port"' > "${COLOR_OUTPUT}"
# reset, turn off all lights
echo 'dec syx 0 32 41 2 16 14 0' >> "${COLOR_OUTPUT}"
echo "dec syx ${SYSEX_HEADER}" >> "${COLOR_OUTPUT}"


row=0
key=0
offset=0

colors=''


# read midimap template file (defined at bottom)
while read -r line; do
  # identify lines that have the magic placeholder <NUMBER>
  if echo "$line" | grep -qE "${REPLACE_START_CHAR}[0-9]+${REPLACE_END_CHAR}"; then

    # key is from 1 to 64 - number of total keys on the launchpad
    # row is from from 1 to 8 - refers to the row on the launchpad
    # offset is for overlapping the same notes across row boundaries 
    # (launchpad firmware defaults this to min 1, but here it can be zero!)
    key=$(( key+1 ))
    if [ $(( key % 8 )) = 1 ]; then
      row=$(( row+1 ))
      if [ "$row" -gt 1 ]; then
        offset=$(( (row-1) * OVERLAP  ))
      fi
    fi


	# shruti_index if from 0 to 21, because it's a bash array
    shruti_index=$(( (key -1 - offset) % (NUM_NOTES_OCTAVE) ))
    color="${COLORS[$shruti_index]}"
    # since this script doesn't yet have tests, echo for poor man's verification
    # printf for left padding
    echo "Key Num `printf %02d $key` - Row $row - Shruti Index `printf %02d $shruti_index` - RGB Color: $color"
    echo "$color" >> "${COLOR_OUTPUT}"

    note=$(( (MIDI_C1_NOTE + TRANSPOSE) + (key - 1) - offset ))
    newline=$(echo "$line" | sed "s/${REPLACE_START_CHAR}${key}${REPLACE_END_CHAR}/@${note}/g")

    # echo "newline is $newline"
    echo "  $newline" >> "${OUTPUT}"

  else
    echo "$line" >> "${OUTPUT}"
  fi
done < "${TEMPLATE}"

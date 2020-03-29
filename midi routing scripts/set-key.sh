#!/usr/local/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ "${BASH_VERSINFO:-0}" -lt 4 ]; then
  if [ -f /usr/local/bin/bash ]; then
    # homebrew bash is installed but was overridden
    echo "\033[1;31mScript interpreter overriden to Bash 3."
    echo "Please ensure script is executable using \`chmod +x set-key.sh\`"
    echo "and invoke using \`./set-key.sh\` instead of \`sh set-key.sh\`\033[0m"
  else 
    echo "\033[1;31mThis script requires Bash version 4 or above."
    echo "Please install using Homebrew: \`brew install bash\`\033[0m"
  fi
  exit 1
fi

if [ "$#" -ne 1 ]; then
    echo -e "\e[1;31mUsage: ./set-key.sh <transpose> "
    echo -e "where transpose is the number of half steps from C3 (can be negative)\e[0m"
    exit 1
fi

# number of overlapping notes across row boundaries 
# launchpad firmware defaults this to min 1, but here it can be zero!
OVERLAP=0

# output files
COLOR_OUTPUT="lpp-colors.smidi"
MIDI_OUTPUT="lpp.txt"

MIDIMAP_TEMPLATE="${DIR}/templates/midimap.template.txt"
ALIAS_PLACEHOLDER=@
REPLACE_START_CHAR='<'
REPLACE_END_CHAR='>'
MIDI_C1_NOTE=36

# read dictionaries
declare -A velocities
while read line; do 
  key=$(echo $line | cut -d "|" -f1)
  data=$(echo $line | cut -d "|" -f2)
  velocities[$key]="$data"
done < "${DIR}/templates/velocities.txt"

declare -A transpositions
while read line; do 
  key=$(echo $line | cut -d "|" -f1)
  data=$(echo $line | cut -d "|" -f2)
  transpositions[$key]="$data"
done < "${DIR}/templates/transpositions.txt"

# number of halfsteps from C
TRANSPOSE="$1"
key_name="${transpositions[${TRANSPOSE}]}"
if [ -z ${key_name} ]; then
    echo -e "\e[1;31mCould not determine key for transposition of ${TRANSPOSE}."
    echo -e "Valid values: -3 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16\e[0m"
    exit 1
fi

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


# initialize output files
echo "" > "${MIDI_OUTPUT}"
echo 'dev "Launchpad Pro Standalone Port"' > "${COLOR_OUTPUT}"
# reset, turn off all lights
echo 'dec syx 0 32 41 2 16 14 0' >> "${COLOR_OUTPUT}"
echo "dec syx ${SYSEX_HEADER}" >> "${COLOR_OUTPUT}"


# initialize counters
row=0
key=0
offset=0

# read midimap template file (defined at bottom)
while read -r line; do

  # identify lines that have the magic placeholder <NUMBER>
  if echo "$line" | grep -qE "${REPLACE_START_CHAR}[0-9]+${REPLACE_END_CHAR}"; then

    # key is from 1 to 64 - number of total keys on the launchpad
    # row is from from 1 to 8 - refers to the row on the launchpad
    # offset is for overlapping the same notes across rows 
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
    note=$(( (MIDI_C1_NOTE + TRANSPOSE) + (key - 1) - offset ))
    velocity="${velocities[${ALIAS_PLACEHOLDER}${note}]}"
    replaced_line=$(echo "$line" | sed "s/${REPLACE_START_CHAR}${key}${REPLACE_END_CHAR}/${ALIAS_PLACEHOLDER}${note} ${velocity}/g")

    # no tests yet, so echo for poor man's verification with fixed width
    echo "Key `printf %02d $key` - Row $row - Shruti `printf %02d $shruti_index` - MIDI `printf %03d $note` - Velocity `printf %03d $velocity` - RGB $color"

    # write to output files
    echo "$color" >> "${COLOR_OUTPUT}"
    echo "  $replaced_line" >> "${MIDI_OUTPUT}"
    echo "$replaced_line"
    
  else
    echo "$line" >> "${MIDI_OUTPUT}"
  fi
done < "${MIDIMAP_TEMPLATE}"

if [ $key -ne 64 ]; then
    echo -e "\e[1;31mScript generation failed.\e[0m"
else
    echo -e "\e[1;32mSuccessfully created ${COLOR_OUTPUT} and ${MIDI_OUTPUT}"
    echo -e "Key set to ${key_name}, ${TRANSPOSE} half steps from C3!"
    echo -e "Start practicing with \`sh start.sh\` 🥳\e[0m"
fi
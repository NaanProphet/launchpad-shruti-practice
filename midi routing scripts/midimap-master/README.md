midimap
=======

Command line tool for generating and mapping MIDI messages for Mac OSX.

Example Use Cases
=================

### Playing a chord when hitting a single button

```
OnNote Any NoteC3 Any
  # if a C3 is hit, then send a C3+E3+G3
  SendNote Channel NoteC3 Value
  SendNote Channel NoteE3 Value
  SendNote Channel NoteG3 Value
End

OnElse
  # if anything else is hit, pass it along
  SendCopy
End
```

### Map a note to the sustain pedal

```
OnNote Any NoteC3 0
  # if C3 is released, release the pedal
  SendLowCC Channel ControlPedal 0
End

OnNote Any NoteC3 Positive
  # if C3 is hit, hit the pedal
  SendLowCC Channel ControlPedal 127
End

OnElse
  # anything else, pass it along
  SendCopy
End
```

### Stop a device from sending Reset commands

```
OnReset Any
  # do nothing
End

OnElse
  # anything else, pass it along
  SendCopy
End
```

### Print out note velocities

```
OnNote Any Any Positive
  # spy on all note hit events and print them
  Print "HIT:" Note Value
  SendCopy
End

OnElse
  # anything else, pass it along
  SendCopy
End
```

### Convert pitch bend to CC parameter change

```
OnBend Any Any
  # convert to ControlGeneral5
  SendLowCC Channel ControlGeneral5 Value
End

OnElse
  # anything else, pass it along
  SendCopy
End
```

### Convert mod wheel to pitch bend

```
OnHighCC Any ControlMod Any
  # convert to pitch bend
  SendBend Channel Value
End

OnElse
  # anything else, pass it along
  SendCopy
End
```

### Send channel 1 notes to all other channels

```
OnNote 1 Any Any
  SendCopy # send to channel 1
  SendNote  2 Note Value
  SendNote  3 Note Value
  SendNote  4 Note Value
  SendNote  5 Note Value
  SendNote  6 Note Value
  SendNote  7 Note Value
  SendNote  8 Note Value
  SendNote  9 Note Value
  SendNote 10 Note Value
  SendNote 11 Note Value
  SendNote 12 Note Value
  SendNote 13 Note Value
  SendNote 14 Note Value
  SendNote 15 Note Value
  SendNote 16 Note Value
End

OnElse
  # anything else, pass it along
  SendCopy
End
```

Usage
=====

```
Usage:
  midimap [--help] [-d] [-f] [-a @alias value]+ [-m "Input Device" <mapfile>]+

  With no arguments specified, midimap will simply list the available sources
  for MIDI input.

  -d   Debug mode (verbose logging)
  -f   Force low CC for all CC values; this is useful for devices that don't use
       high CC at all, and treats all CC messages as low resolution
  -a @alias value
       Create an alias; aliases can be used for giving meaningful names to
       numbers, controllers, or RPN parameters
  -m "Input Device" <mapfile>
       Listen for messages from "Input Device", and apply the rules outlined
       in the <mapfile> for every message received
  -h   Help
  -v   Print version and exit

  The program will output the results to a single virtual MIDI device, named
  in the format of "midimap", "midimap 2", "midimap 3", etc, for each
  copy of the program running.

Input Devices:
  The program will always list out the available input devices.  For example:
    Source 1: "Keyboard A"
    Source 2: "Keyboard B"
    Source 3: No Name Available
    Source 4: "Pads"
    Source 5: "Pads"

  Sources can be specified using the name:
    midimap -m "Keyboard A" <mapfile>
  Or the source index:
    midimap -m 5 <mapfile>

Map Files:
  Map files consist of a list of event handlers and aliases.  If the handler's
  criteria matches the message, the instructions in the handler are executed,
  and no further handlers are executed.

    Alias @TargetChannel 16

    OnNote 1 NoteGb3 Any
      # Change the Gb3 to a C4
      Print "Received:" Channel Note Value
      SendNote @TargetChannel NoteC4 Value
    End

  For this example, if the input device sends a Gb3 message at any velocity in
  channel 1, the program will print the message, and send a C4 instead on
  channel 16.

  The OnNote line is what message to intercept, and the matching criteria
  for the message.  Criteria can be a literal value, `Any` which matches
  anything, or `Positive` for a number greater than zero.  Inside the handler,
  the instructions are executed in order using raw values ("Received:", 16,
  NoteC4) or values dependant on the original message (Channel, Note, Value).

  Any line that begins with a `#` is ignored and considered a comment.

  All event handlers end with `End`.

  Event Handlers:
    OnNote         <Channel> <Note> <Value>     Note is hit or released
    OnBend         <Channel> <Value>            Pitch bend for entire channel
    OnNotePressure <Channel> <Note> <Value>     Aftertouch applied to note
    OnChanPressure <Channel> <Value>            Aftertouch for entire channel
    OnPatch        <Channel> <Value>            Program change patch
    OnLowCC        <Channel> <Control> <Value>  Low-res control change
    OnHighCC       <Channel> <Control> <Value>  High-res control change
    OnRPN          <Channel> <RPN> <Value>      Registered device parameter
    OnNRPN         <Channel> <NRPN> <Value>     Custom device parameter
    OnAllSoundOff  <Channel>                    All Sound Off message
    OnAllNotesOff  <Channel>                    All Notes Off message
    OnReset        <Channel>                    Reset All Controllers message
    OnElse                                      Messages not matched

  Parameters:
    Channel   MIDI Channel (1-16)
    Value     Data value associated with event (see details below)
    Note      Note value (see details below)
    Control   Control being modified (see table below)
    RPN       Registered parameter being modified (see table below)
    NRPN      Non-registered parameter being modified (0-16383)

  "Value" is a number that depends on the event:
    OnNote          Velocity the note was hit (0-127) Use 0 for note off
    OnBend          Amount to bend (0-16383, center at 8192)
    OnNotePressure  Aftertouch intensity (0-127)
    OnChanPressure  Aftertouch intensity (0-127)
    OnPatch         Patch being selected (0-127)
    OnLowCC         Value for the control (0-127)
    OnHighCC        Value for the control (0-16383)
    OnRPN/OnNRPN    Value for the parameter (0-16383)

  Notes:
    Notes are represented in the format of:
      `Note<Key><Octave>`
    Where Key can be one of the 12 keys, using flats:
      Key = C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B
    And Octave can be one of the 11 octaves, starting at -2 (represented as N2):
      Octave = N2, N1, 0, 1, 2, 3, 4, 5, 6, 7, 8

    The last addressable MIDI note is NoteG8, so NoteAb8, NoteA8, NoteBb8 and
    NoteB8 do not exist.

    Therefore, the entire range is: NoteCN2, NoteDbN2, ... NoteF8, NoteG8.

  Low-Resolution Controls (MIDI hex value in parenthesis for reference):
    ControlPedal      (40)          ControlGeneral5    (50)
    ControlPortamento (41)          ControlGeneral6    (51)
    ControlSostenuto  (42)          ControlGeneral7    (52)
    ControlSoftPedal  (43)          ControlGeneral8    (53)
    ControlLegato     (44)          ControlPortamento2 (54)
    ControlHold2      (45)          ControlUndefined1  (55)
    ControlSound1     (46)          ControlUndefined2  (56)
    ControlSound2     (47)          ControlUndefined3  (57)
    ControlSound3     (48)          ControlVelocityLow (58)
    ControlSound4     (49)          ControlUndefined4  (59)
    ControlSound5     (4A)          ControlUndefined5  (5A)
    ControlSound6     (4B)          ControlEffect1     (5B)
    ControlSound7     (4C)          ControlEffect2     (5C)
    ControlSound8     (4D)          ControlEffect3     (5D)
    ControlSound9     (4E)          ControlEffect4     (5E)
    ControlSound10    (4F)          ControlEffect5     (5F)
    ControlReserved1  (66)          ControlReserved2   (67)
    ControlReserved3  (68)          ControlReserved4   (69)
    ControlReserved5  (6A)          ControlReserved6   (6B)
    ControlReserved7  (6C)          ControlReserved8   (6D)
    ControlReserved9  (6E)          ControlReserved10  (6F)
    ControlReserved11 (70)          ControlReserved12  (71)
    ControlReserved13 (72)          ControlReserved14  (73)
    ControlReserved15 (74)          ControlReserved16  (75)
    ControlReserved17 (76)          ControlReserved18  (77)

  High-Resolution Controls (MIDI hex values in parenthesis for reference):
    ControlBank           (00/20)   ControlGeneral1    (10/30)
    ControlMod            (01/21)   ControlGeneral2    (11/31)
    ControlBreath         (02/22)   ControlGeneral3    (12/32)
    ControlUndefined6     (03/23)   ControlGeneral4    (13/33)
    ControlFoot           (04/24)   ControlUndefined10 (14/34)
    ControlPortamentoTime (05/25)   ControlUndefined11 (15/35)
    ControlChannelVolume  (07/27)   ControlUndefined12 (16/36)
    ControlBalance        (08/28)   ControlUndefined13 (17/37)
    ControlUndefined7     (09/29)   ControlUndefined14 (18/38)
    ControlPan            (0A/2A)   ControlUndefined15 (19/39)
    ControlExpression     (0B/2B)   ControlUndefined16 (1A/3A)
    ControlEffect6        (0C/2C)   ControlUndefined17 (1B/3B)
    ControlEffect7        (0D/2D)   ControlUndefined18 (1C/3C)
    ControlUndefined8     (0E/2E)   ControlUndefined19 (1D/3D)
    ControlUndefined9     (0F/2F)   ControlUndefined20 (1E/3E)
                                    ControlUndefined21 (1F/3F)

  If -f mode is used, then high-resolution controllers are interpreted as
  two separate low-resolution controllers.  These are identified by taking
  the high-resolution controller name and adding MSB or LSB to the end.
  For example:
    ControlBank (00/20) becomes:  ControlBankMSB (00)  ControlBankLSB (20)
    ControlMod  (01/21) becomes:  ControlModMSB  (01)  ControlModLSB  (21)
    ...etc
  The -f mode also disables RPN/NRPN conrols, and instead interprets the
  CC messages as low-resolution controllers with the names:
    ControlDataMSB       (06)       ControlDataLSB       (26)
    ControlPNIncrement   (60)       ControlPNDecrement   (61)
    ControlNRPNSelectLSB (62)       ControlNRPNSelectMSB (63)
    ControlRPNSelectLSB  (64)       ControlRPNSelectMSB  (65)

  Registered Parameters (MIDI hex values in parenthesis for reference):
    RPNBendRange     (00/00)        RPNAzimuth          (3D/00)
    RPNFineTuning    (00/01)        RPNElevation        (3D/01)
    RPNCoarseTuning  (00/02)        RPNGain             (3D/02)
    RPNTuningProgram (00/03)        RPNDistanceRatio    (3D/03)
    RPNTuningBank    (00/04)        RPNMaxDistance      (3D/04)
    RPNModRange      (00/05)        RPNGainAtMax        (3D/05)
    RPNEmpty         (7F/7F)        RPNRefDistanceRatio (3D/06)
                                    RPNPanSpread        (3D/07)
                                    RPNRoll             (3D/08)

  Aliases:
    Any number, Note*, Control*, or RPN* keyword can be aliased to another
    keyword starting with @.  For example, if your MIDI controller sends
    ControlReserved1 when hitting the play button, you can alias it via:

      Alias @PlayChannel  1
      Alias @PlayButton   ControlReserved1

    Then, it can be referenced anywhere else, like:

      OnLowCC @PlayChannel @PlayButton Positive
        # play was hit...
      End

    Aliases can also be defined from the command-line using -a:
      midimap -a @PlayChannel 1 -a @PlayButton ControlReserved1 ...etc...

  Commands:
    Print "Message" "Another" ...                    Print values to console
      (`Print RawData` will print the raw bytes received in hexadecimal)
    SendCopy                                         Send a copy of the message
    SendNote         <Channel> <Note> <Value>        Send a note message, etc
      (Use 0 for Value to send note off)
    SendBend         <Channel> <Value>
    SendNotePressure <Channel> <Note> <Value>
    SendChanPressure <Channel> <Value>
    SendPatch        <Channel> <Value>
    SendLowCC        <Channel> <Control> <Value>
    SendHighCC       <Channel> <Control> <Value>
    SendRPN          <Channel> <RPN> <Value>
    SendNRPN         <Channel> <NRPN> <Value>
    SendAllSoundOff  <Channel>
    SendAllNotesOff  <Channel>
    SendReset        <Channel>
```

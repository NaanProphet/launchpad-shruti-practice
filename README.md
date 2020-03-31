# launchpad-shruti-practice

Using a Novation Launchpad Pro to practice the 22 shrutis of Indian classical music.

![Picture of the Novation Launchpad Pro with 22 shrutis colors](docs/launchpad-pic.jpg)

## Demos

Hearing is believing! Quick 15 second demos of various ragas encompassing 16 of the 22 shrutis.

Each demo features the arohi (ascending scale) and avarohi (descending scale), and concludes with a faster swar mandal-like descending flourish that really brings out the combined, blending consonance aka mood (bhava) of the raga.

Particularly interesting notes to listen for are indicated in bold.

**Bhoopali** 

S R2 **G1** P **D1** S' | S' **D1** P **G1** R2 S

<iframe width="100%" height="100" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/787249084%3Fsecret_token%3Ds-qjaBZFcWRqr&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

**Shivranjani** 

S R2 **g2** P **D2** S' | S' **D2** P **g2** R2 S

<iframe width="100%" height="100" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/787249075%3Fsecret_token%3Ds-gWia1w5Q1Oi&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

**Yaman** 

**N1** R2 **G1** **m1** **D2** **N1** S' | S' **N1** **D2** P **m1** **G1** R2 S

<iframe width="100%" height="100" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/787249072%3Fsecret_token%3Ds-EfY5qlr6UBp&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

**Desh** 

S R2 M1 P **N1** S' | S' **n1** **D1** P M1 **G1** R2 S

<iframe width="100%" height="100" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/787249069%3Fsecret_token%3Ds-a9ih4OL2zck&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

**Bheempalasi** in Madhyam tuning (would give **R1** extra bolding if I could!)

<u>**n1**</u> S **g1** M1 P **n1** S' | S' n1 **D1** P M1 **g1** **R1** S 

<iframe width="100%" height="100" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/787249066%3Fsecret_token%3Ds-szl5lvxJRJC&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

**Bhairavi** (M2 and n2 are especially bold here!)

S **r2** **g2** **M2** P **d2** **n2** S' | S' **n2** **d2** P **M2** **g2** **r2** S

<iframe width="100%" height="100" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/787249057%3Fsecret_token%3Ds-n74LIeBAris&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>

More about the tuning in the [Shruti](#shruti-colors) section.

## Prerequisites

* Launchpad Pro
  - Only Pro supports Programmer aka custom MIDI mode and RGB colors
* Mac OS X
  - Tested on 10.14 Mojave
  - [Midimap](https://github.com/voidqk/midimap) for Mac (prebundled)
* Native Instruments
  - Kontakt Player
    - Free player is OK to use the already exported pratice sets `.nki` files. Otherwise the paid version is required to access the script editor (see below)
  - Kontakt Factory Library
    - Used for the playable Tanpura
    - Specifically just the `World/6 - Strings/Tanpura.nki` sample
  - [India Discovery Series](https://www.native-instruments.com/en/products/komplete/world/india/) (optional)
    - For the background tanpura, very rich sound

See [Native Instruments Komplete Version Comparison](https://docs.google.com/spreadsheets/d/1C2lEubeNV6OzUnj5o8o6pBPU_jGgzeCALNTLOnoPxeA/edit?usp=drive_web&ouid=113346694824160986526) for an awesome spreadsheet to help identify which Komplete bundles contain these libraries.

## How to Use

1. Connect the Launchpad Pro via USB and enter Programmer Mode. See the [Launchpad Pro User Guide](https://resource.novationmusic.com/support/product-downloads?product=Launchpad+Pro) for details.

2. Open Terminal and run the background MIDI daemon: `sh start.sh`

3. Double click the `Shruti Practice.nkm` practice file to launch/reload Kontakt/Kontakt Player

4. Open MIDI Preferences. Turn off mapping for default Launchpad inputs. Set `midimap` to Port A. ![Setting up midimap routing in Kontakt](docs/kontakt-midimap.gif)

5. Adjust the key root. By default the scale is set to C. (The demo below shows how to adjust it to D i.e. two half steps.)

   1. Set the `Tune` parameter to the number of half steps in the top, playable instrument.
   2. Set the `Root` key in the second background tanpura instrument.
   3. Press the ▶️ icon to start the background tanpura. ![Setting the scale/key root for the tanpuras](/Users/Krish/Documents/GitHub/launchpad-shruti-practice/docs/kontakt-adjust-root.gif)
   4. To adjust tuning of Concert A (default 440Hz), open the `Master` pane and adjust the `Master Tune` parameter as needed. ![Adjusting the value of A440 Hz globally](docs/kontakt-adjust-a440.gif)

6. Save your settings to a new file by clicking `Load/Save` (floppy disk icon) > `Save Multi as...` ![Saving settings to a new file](docs/kontakt-saving-settings.gif)

## Shruti Colors

The ratios of the 22 shrutis used are the same as those defined and researched by Dr. Vidyadhar Oke. The RGB values are sent via Sysex commands and are specified in `lpp-colors.smidi`.

| **Shruti** | **Ratio** | **ET Offset (Cents)** | **Launchpad RGB** | **Color**    |
| ---------- | --------- | --------------------- | ----------------- | ------------ |
| S          | 1         | 0.0                   | 25 25 25          | White        |
| r1         | 256/243   | -9.8                  | 30 2  2           | Red          |
| r2         | 16/15     | 11.7                  |                   |              |
| R1         | 10/9      | -17.6                 |                   |              |
| R2         | 9/8       | 3.9                   | 0  10 0           | Green        |
| g1         | 32/27     | -5.9                  | 5  5  63          | Blue         |
| g2         | 6/5       | 15.6                  |                   |              |
| G1         | 5/4       | -13.7                 |                   |              |
| G2         | 81/64     | 7.8                   | 0  80 80          | Aquamarine   |
| M1         | 4/3       | -2.0                  | 24 8  0           | Light Orange |
| M2         | 27/20     | 19.6                  |                   |              |
| m1         | 45/32     | -9.8                  |                   |              |
| m2         | 729/512   | 11.7                  | 15 2  0           | Red-Orange   |
| P          | 3/2       | 2.0                   | 33 20 0           | Yellow       |
| d1         | 128/81    | -7.8                  | 70 0  40          | Dark Purple  |
| d2         | 8/5       | 13.7                  |                   |              |
| D1         | 5/3       | -15.6                 |                   |              |
| D2         | 27/16     | 5.9                   | 18 9  20          | Light Purple |
| n1         | 16/9      | -3.9                  | 30 10 10          | Light Pink   |
| n2         | 9/5       | 17.6                  |                   |              |
| N1         | 15/8      | -11.7                 |                   |              |
| N2         | 243/128   | 9.8                   | 80 0  10          | Magenta      |

## Build Requirements

This would be if you want to start from scratch and/or support new tunings.

* [Homebrew](https://brew.sh)
  * To install simply run: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`
* [Scala by Manuel Op de Coul](http://www.huygens-fokker.org/scala/index.html) (not the language) for generating Kontakt Script files
  * I suppose these can be done by hand as well but 🤷🏾‍♂️
  * Included `bundle-scala.sh` uses Wine to bundle a runnable App! (Mac instructions on website badly out of date.)
* Kontakt 5 or [Kontakt 6](https://www.native-instruments.com/en/products/komplete/samplers/kontakt-6/) in order to access the instrument editor (wrench icon)

  - Tested with Kontakt 5.8.1
* Bash 4 or greater 
  * Can be installed with Homebrew: `brew install bash`
  * Used by the `set-key.sh` script

## Remarks

* First attempted the Discovery Series tanpura for the playable tanpura as well. However the playable MIDI range 48-84 is enforced _before_ the Kontakt remapping script and does not seem to be able to be turned off even with the Script Editor. In a way, the Kontakt Factory Library tanpura offers a less twangy and more consistent sound suitable for a playable swar mandal instrument.


## Additional Reading

* [Microtuning in Kontakt 5 and 6](https://soundbytesmag.net/technique-microtuning-in-kontakt-5-and-6/) by Warren Burt, Jan. 2019.
* [22shruti.com](http://22shruti.com) Dr. Vidyadhar Oke's website featuring articles, TEDx talks and demos.
* [Wilsonic](https://apps.apple.com/us/app/wilsonic/id848852071) App for iOS. Great for exploring various tunings. Exports Scala tuning files.
* [Peterson Strobe Tuners](https://www.petersontuners.com) for highly accurate tuners that support custom tunings aka "sweeteners". Included one for the 22 shrutis on the [User Trading Post](https://www.petersontuners.com/sweeteners/shared/) (listed under `World` > `SRU`).


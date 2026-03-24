# GPI to OSC
A **ready to use** repo which takes any GPI input and converts them to specific [OSC messages](https://opensoundcontrol.stanford.edu/spec-1_0.html). The library can be used and adopted for any use case but the example is built around a **RasPi** which takes GPI input and converts them to **OSC** for use in [TallyArbiter](https://tallyarbiter.com/).
<br/>This whole documentation is really detailed as it's aimed to be used by anyone in the industry even someone who never worked with RasPi's, GitHub or Linux.
<br/>
<br/>
## DOCS
- [Intended use with **TallyArbiter**](#use-with-tallyarbiter)

- [Showcase](#repo-in-use)

- [Basic inner workings](#how-does-it-work)

- [Example files for other use cases](#further-examples)
<br/>

## TODO'S

- [ ] Create Docs
- [ ] Fully show and describe installation process and cron setup for someone who is not familiar with RasPi and Linux
- [ ] Sample Files for different devices
- [ ] Move HTML from hardcoded to its own file
- [ ] Either implement [python-osc](https://python-osc.readthedocs.io/en/latest/) or build own OSC message builder instead of hardcoded messages
- [ ] Build functions and fundamentals as library instead of purpose-built for just one use case
<br/>

## Use with TallyArbiter
> [!NOTE]
> The repo in its current state is made for specific use of a RasPi to convert incoming GPI (for example from a [videoswitcher](https://www.blackmagicdesign.com/products/atemconstellation)) to OSC messages, which get send to a Tally Arbiter server. Other use cases require some tinkering but can use this repo as a base.

### Getting started
Download both the gpi_osc.py and web_config.py files onto your RasPi. Now run both files and the Pi will automatically create an initial config.ini file and also start its own webserver on *hostname*.local:8000. By visiting this webpage you can configure your Pi. Additionally it's encouraged to run the files automatically after boot via [cron](https://wiki.ubuntuusers.de/Cron/)
<br/>
<br/>

***Basic config - RasPi***
> [!IMPORTANT]
> The basic config **must** be changed in order for the program to work, as your individual Tally Arbiter IP address and port are needed.
> 
Visit the webpage under *hostname*.local:8000 (for our example TallyGPI.local:8000) and put in your server IP, port and also change your GPI pins[^1].
<br/>
[^1]: Optionally you can use the gpi_osc.py standalone and change the config.ini locally on your RasPi
*image_placeholder*
<br/>
<br/>

***Basic config - Tally Arbiter***
<br/>
In order for the server to correctly receive the OSC messages you need to configure a proper source device.
<br/>
<br/>

**`Source Config:`**
> Source Type: `OSC` <br/>
> Source Name: `Your Name` <br/>
> Port: `Your Port`
>
<img src="https://imgur.com/63xpxTJ.png" alt="Add Source" style="width:40%; height:auto;">
<br/>
<br/>

**`Device Config:`**
> Device Name: `Camera ID/Name` <br/>
> TSL Address: `Your Camera Number -1`
>
<img src="https://imgur.com/LGhsq6d.png" alt="Device Config" style="width:40%; height:auto;">
<br/>
<br/>

**`Device Source Config:`**
> Source: `Your OSC Source` <br/>
> Input/Address Number: `Your Camera Number`
>
<img src="https://imgur.com/XbXiCvr.png" alt="Device Source" style="width:60%; height:auto;">
<br/>
<br/>

**`Full Example Config:`**
<br/>
<img src="https://imgur.com/3oJ1dCA.png" alt="Config Overview" style="width:50%; height:auto;">
<br/>
<br/>

## Repo in use
Here's a showcase of the repo in use in a production environment
<br/>
*video_placeholder*
<br/>
<br/>

## How does it work?
Essentially the Pi sets up it's GPI pins as buttons. When they are pulled high the virtual button is pressed, when pulled low it's released. On a virtual button press the Pi builds an OSC message which sends a command with the proper layout to the Tally Arbiter server.
<br/>

**OSC message layout**
> `/tally/program_on/1` --> where `/tally` is the basic address,  `/program_on`  is the command to turn on the tally and  `/1` is the address of the camera that's targeted<br/>
> <br/>
> Further commands that are possible but only included in the example.py for other use cases are: ```/preview_on|/preview_off /previewprogram_on|previewprogram_off``` --> learn more here [TallyArbiter Docs](https://josephdadams.github.io/TallyArbiter/docs/usage/sections/sources#open-sound-control-osc)
> 
<br/>
<br/>

## Further examples
> [!WARNING]
> These examples aren't fully tested due to lacking hardware on my end and may also not be fully documented.
>

prv_pgm.py -->
> In this example python-osc is implemented as the OSC message builder and 2 cameras with PGM and PRV are configured
>

esp32.py -->
> Setting up an ESP32 as the one handling GPI to OSC. Far cheaper than RasPi and not as overpowered.
>

test.py -->
> more coming.....
>
<br/>
<br/>

## Contributions
....
<br/>
<br/>

## Credits
....
<br/>
© 2026 Gamic
<br/>

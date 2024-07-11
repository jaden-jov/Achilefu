# Handheld CVG Notes

**Important**: check waveshare.io cm4 documentation for necessary changes to boot config to recognize the imx219 cameras

## PROBLEM

Implement GStreamer with the handheld part of the CVG to reduce the bulk added by the HDMI transmitter, and find an IR excitation source

## BRAINSTORN

1. Ian's thing, would require some system to process the data from the pi 
	zero and send it to the headset, which would probable have to just switch 
	inputs. This method means the handheld would contain the NIR camera, some 
	type of rpi, power, and hdmi transmitter. Downsides include bulk of it and
	that it has to be switched through hardware, not software.
2. streaming application, instead of getting an input from the rpi 
	in the headset it could get input from the rpi in the handheld, this would 
	probable be the easiest route to do this. The handheld would contain the pi
	or whatever else he's using, power, cameras, and hdmi im assuming? Need to 
	get more info on this but it's the most promising option

## PLAN

### NIR Light Source:
1. Look into options **COMPLETED**
2. Contact Lumixtar **COMPLETED, no way to establish contact**
3. Take apart the laser modules and try to find a way to make the smaller

### Gstreamer
1. establish a working single camera pipeline **COMPLETED**
2. write a program that switches between displaying two streams with a keyboard input
3. write the pi side program to turn the stream off when not displayes (optional)

## RESOURCES
-https://www.laserlands.net/diode-laser-module/780nm-ir-laser-
			module/industrial-focusable-50mw-780nm-infrared-ir-laser-dot-diode-
			module-lazer.html
-The light source module consists of five 200 mW LDs at a central 
			wavelength of 760 nm.
-10 W near-infrared LED from eBay, which emits light with a wavelengthof 
			780 nm (price: $18), as well as a 10 W LED driver for this LED 
			(price: $3). We placed a special filter in front of the camera with 
			the following parameters: center wavelength 832 nm, 10 nm width 
			bandpass filter.
-https://luminus.com/products/ir
-https://www.lumixtar.com/5w-ir-780nm-high-power-led.html
-https://www.lumixtar.com/smd3030-1w-ir-780nm-led.html
-https://www.ebay.com/itm/235015636599 << convex lens 20 degrees
-https://www.laserlands.net/laser-diode/780nm-diode/11071132.html

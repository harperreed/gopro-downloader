# GOPRO Downloader

### Moves images from the gopro to the local filesystem

I needed a solution that would allow a client (in this case a raspberry pi) to connect to the gopro wifi and download all of the images available. 

Once the image has been downloaded, the script will delete the image. 

The original script was made by @KonradIT and was included in their [raspberrypi-gopro](https://github.com/KonradIT/raspberrypi-gopro) repo. They have also documented the API that the gopro uses [here](https://github.com/KonradIT/goprowifihack).
Download All Media over WiFi


### Goal

The goal is to have a simple script that I can run on a cron that will download all the images from a gopro semi-regularly (every hour on the hour). I also want to remove the images from the gopro so that i don't have to swap SD cards. 


### My setup

I will have a gopro and a blinkx mounted in a weather proof container on a location with wifi. Using this script, A raspberry pi will grab the images from the gopro and stich them into a timelapse video. 

### Future

* no idea. maybe push images to s3 or something


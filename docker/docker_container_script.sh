#!/bin/bash

docker build -t my_custom_image . 

if [ $? -eq 0 ]
then
	#Delete the container built against the previous image
	docker container rm my_container
	docker run -it --name my_container my_custom_image
else
	exit 1
fi
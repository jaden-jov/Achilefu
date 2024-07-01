Config for all this includes changing config.txt to recognize the imx219 cameras, that should be it
original pipeline didn't work because bookworm uses libcamera so the first element of the pipeline is different than buster, I thought it was the memory allocation but bookworm doesn't allocate memory

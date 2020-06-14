# Distance Sensors Setup

The distance sensor code uses GPIOZero. Be sure to install the version mentioned in chapter 8.

# Menu Server Setup

You will need to install Flask for this step.

    pi@myrobot:~ $ pip install flask

# Additional Troublexhooting Notes

The book has a number of troubleshooting notes. Please check those first. If these are still not working, try the following additional troubleshooting steps:

* Not all logic level shifters are bidirectional - please ensure the type you have used state bidirectional in their description.
* Some logic level shifters will need a 3v (lv) power connection from the lower volt rail on the breadboard.

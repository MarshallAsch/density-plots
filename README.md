![Code linter on main](https://img.shields.io/github/workflow/status/marshallasch/density-plots/Clang-format/main?style=plastic)
![ns3 build checker on main](https://img.shields.io/github/workflow/status/marshallasch/density-plots/build-ns3/main?style=plastic)
![GitHub](https://img.shields.io/github/license/marshallasch/density-plots?style=plastic)
![Lines of code](https://img.shields.io/tokei/lines/github/marshallasch/density-plots?style=plastic)
![NS3 version](https://img.shields.io/badge/NS--3-3.32-blueviolet?style=plastic)

# Random Waypoint Mobility Model Test

This repository holds the code that is used to run the ns-3 simulations to generate the data and produce the density plots comparing several locations in canada.

This code was written for use with the ns-3.32 simulator and is designed to be run from within the scratch folder. 


Generated the locations using the gen_coverage file using ns3
I chose to use ns3 so that the same position allocator that is used for the actual simulation is also used to produce these figures


population densities were multiplied by 25 to get the number of nodes in a 5km area.

after rounding the following values were used:
- Minden  : 172
- Rigolet : 2110
- University of Guelph : 37777
- Toronto : 108360

nodes were assigned a set of random (x,y) coordinated from a uniform random distribution.

The seed and run values for the random number generator were set at '3' and '1' respectively for each of the 4 generations.

The x and y locations were extracted from the trace files for each node and was plotted with a python script with a 50m radius around it
the 50m is to signify the wifi range.


## Prereqs:

`pip install matplotlib argparse`


If building netanim:
- qt4-qmake
- libqt4-dev

(additionally, on ubuntu 20.10, you need to add an additional repo because qt4 no longer ships with it)
- https://launchpad.net/~gezakovacs/+archive/ubuntu/ppa

## Building this project

Reproducibility is one of the key goals of simulator studies.

 1. Download and build copy of the ns-3.32 all-in-one distribution.

    ```sh
    wget https://www.nsnam.org/release/ns-allinone-3.32.tar.bz2
    tar xjvf ns-allinone-3.32.tar.bz2
    cd ns-allinone-3.32
    python3 ./build.py --enable-examples --enable-tests
    ```

 2. Change directories to the `scratch/` folder of the ns-3.32 source
    distribution.

    ```sh
    cd ns-3.32/scratch/
    ```

 3. Clone this repository.

    ```sh
    git clone git@github.com:marshallasch/density-plots.git plots
    ```

4. Change directory back to the `ns-3.32` folder of the source distribution
   and re-configure `./waf` so it can cache the new changes

   ```sh
   cd ..
   ./waf configure --enable-examples --enable-tests
   ./waf build
   ```

5. Run the example simulation that is included within the module.

   ```sh
   ./waf --run 'scratch/plots/plots'
   ```
   
   This will generate an netanim xml file called `<city>.xml`
   This file will have multiple different entry types, for this plot we only care about the node locations. 

6. extract the node locations

   Filter the file to only include the node locations

   ```bash
   $ grep -E "^<node.*/>$" city.xml > filtered.txt
   ```

7. The plot script expects a space separate list of node locations for a single time interval, so that each node only gets plotted once. 

   ```bash
   $ cat filtered.txt | cut -d '"' -f 6,8 | sed -E 's/"/ /'  > coordinates.txt
   ```

7. run `./genPlots.py --city Minden --range 50 --density 6.9 coordinates.txt` to generate the plot that shows a 5km x 5km area and the coverage from the number of devices from the population density.

# K-Ripley-s-Function
Modified version of K-Ripley's function, specific for clustering analysis of fluorescent images

Prior requirements to using this code involves a (1) directory list of items which have been presorted, (2) imagej/Fiji array data, (3) Python and the (4) relevant packages required to run this analysis. 

(1) Directory list

A listed directory is important for sorting data and telling the computer where specific file names will occur. Our code 'loops' through a set of files within a 'directory' and obtains a txt file from each file and uses it to gather data. The essential key here is to have universal directories with similar routes for searching. In our case, specified file names aren't nesseccary however a specific directory is initially required to tell the computer where everything is. We have three main directories, named after each autophagy receptor and within each we have a list of files that look like this:

<img src='https://i.imgur.com/XzdN5HR.png' width = '300'>

Note that we have four levels for test conditions and all repeats are present. I am still trying to find a way to streamline this approach but for now all we can do is just make all the files and duplicate them into other directories.

(2) Array data

Now we have sorted files we can add information to them. On Fiji/Imagej you can access pixel data in a text file and save it to specified directories. If you have images separate the channels and assign a different name for each channel. To take pixel data from imageJ: ANALYSE -> TOOLS -> Save XY coordinates

<img src = "https://media.giphy.com/media/Fu7dQWS1h3SrvrSnwH/giphy.gif" width = "1000">

(3) Python

Now we need to download python: https://www.python.org/downloads/ 
There are several steps that I recommend using virtual environments in python so all packages which are downloaded can be specified but this is not a requirement, more so for organisation purposes. You can have a look at them here: https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a%20Python%20environment%20such,directory%20tree%20which%20contains%20Python%20executable%20files%20

Now python is downloaded you have to specify a PATH for its environment. Essentially, a path is specified so that Python knows where to access it's packages. 

(3) Packages

<img src = "https://media.giphy.com/media/jmGYwLDl4XR9fNfULT/giphy.gif" width = "1000">

This is how you download packages to your internal environment and running python should automatically recognise the PATH variable. If you get an error which says PIP is not a available, e-mail me. Now just like in the gif go to the python file calle K-Clustering.py and look at all the imports and 'pip install them all'. If it doesn't work: error 'package does not exist' then it probably has another name.

(4) Running the code


# Doubting Thomas Explorer
A set of scripts to explore the bible through cross references
<p align="center">
  <img src='images/runstepper_gif.gif' width="500px" />
</p>
## How to Use
First, download or clone the repo
```
git clone https://github.com/owenauch/doubting-thomas-explorer.git
```

### Cross Reference Stepper:
View cross references of specified start verse with ability to branch recursively (shown above)
* Run ```runstepper.py``` with python: ```doubting-thomas-explorer/scripts/runstepper.py```
* Enter start verse when prompted
* View cross references of any verse output by entering its number, or exit by entering "n"


### Cross Reference Explorer:
Run a depth-first exploration from a specified start verse and format to a csv file
* Run ```thomascsv.py``` with python: ```doubting-thomas-explorer/scripts/thomascsv.py```
* Enter start verse and depth of search when prompted
* View "verses.csv" in ```scripts``` folder of repo


### Requirements
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/#Download)

### Contributing
Contributions are welcome and encouraged! Here's how to contribute:
 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

Furthermore, if you spot a bug or have an idea, please submit it to [issue tracking](https://github.com/owenauch/doubting-thomas-explorer/issues).

**List of improvements to make and features to add:**
* Improvements to cross reference exploration algorithm (efficiency, ensuring no infinite loops, etc)
* Dealing with references to multiple verse passages (ex. Matthew 10:1-5)
* Front-end to display Verse objects as a connected graph
* Statistical analysis of cross reference data
* Someone with a better computer than me to run the search algorithm for a really long time (mine crashes)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## John 20:24-29
**24** Now Thomas (also known as Didymus), one of the Twelve, was not with the disciples when Jesus came. **25** So the other disciples told him, “We have seen the Lord!”

But he said to them, “Unless I see the nail marks in his hands and put my finger where the nails were, and put my hand into his side, I will not believe.”

**26** A week later his disciples were in the house again, and Thomas was with them. Though the doors were locked, Jesus came and stood among them and said, “Peace be with you!” **27** Then he said to Thomas, “Put your finger here; see my hands. Reach out your hand and put it into my side. Stop doubting and believe.”

**28** Thomas said to him, “My Lord and my God!”

**29** Then Jesus told him, “Because you have seen me, you have believed; blessed are those who have not seen and yet have believed.”

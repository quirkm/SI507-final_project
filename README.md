# SI507-final_project

In this project, you are able to traverse an online fungi identification guide through your own command tool line functionality. 

The data formatted within the series of webpages are accessed as a hierarchical tree organization. Thus, my project works by traversing the tree structure rather than creating it. 

The program will greet you and ask you to proceed when you're ready. It will then provide you with 26 different families of fungi. You are asked to then choose one family to learn more about the family and its members. 

Upon selecting a family, you'll be asked if you want to learn more information about the family in general or if you'd like to select a species of the family to learn more about that species. Even if you select to learn more general family information first, you'll be given the option to select a species after. 

Once you select a specific species, there is a host of different dimensions you will be given the option to type and learn more about that species. 

After each input prompt, you'll be given options to go back and select a new species within that family or go back to the beginning and select a new family to traverse through. Or you can just exit the program completely. 

Happy foraging!



Required packages:
- requests
- BeautifulSoup
- time
- shutil
- matplotlib.pyplot as plt
- matplotlib.image as mpimg
- json

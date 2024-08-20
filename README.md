# JavaScript Code Sorter and Classifier

## Overview

This program is designed to automatically analyze, sort, and restructure JavaScript code files. It organizes code blocks, such as classes, functions, and imports, according to predefined rules, making the code more readable and maintainable. The program also generates a summary header comment that provides a high-level overview of the different elements in the code.  

## Features

- **Code Block Sorting:** Automatically sorts various JavaScript code blocks, such as classes, methods, and functions, according to specified rules.  
- **Code Classification:** Identifies and classifies different code elements (e.g., imports, exports, comments) and organizes them in a structured manner.  
- **Header Comment Generation:** Creates a summary header comment that outlines the structure of the code, including the names and types of elements.  
- **Empty Line Management:** Limits the number of consecutive empty lines and removes trailing empty lines, ensuring clean and consistent code formatting.  
- **Customization:** Allows for customization of sorting and classification rules through easy-to-modify dictionaries.  

## Usage

### Requirements

- JavaScript-code-structure-detection (in my repo)  
- Python 3.x
- `numpy` library

### Running the Program

1. **Setup:**
   - Place your JavaScript files in the specified folder or list the files directly in the script.

2. **Execution:**
   - Run the script. It will process each JavaScript file, reorder and classify its contents, and save the newly structured code into a new file with a `_new` suffix.

### Configuration

- **Code Elements Configuration:**
  - `singles`: A dictionary that defines single-line elements (e.g., imports, comments) and their positions in the code.
  - `blocks`: A dictionary that defines multi-line code blocks (e.g., classes, functions) and how they should be sorted and positioned.

- **File Processing:**
  - Modify the `folder` and `files_name` variables to specify the folder and files you want to process.
  - The script processes all JavaScript files within the specified folder, excluding those with a `_new` suffix.

### Example

Suppose you have a file named `example.js` that you want to process. The script will reorder and classify the contents of `example.js` and save the output as `example_new.js`.

### Output

- **Reordered Code:**
  - The resulting code will have all elements sorted and positioned according to the rules specified in the script.
  - A header comment summarizing the elements in the code will be added at the top.

- **Formatted Code:**
  - The code will have a consistent format, with limited consecutive empty lines and no trailing empty lines.

## Customization

You can easily adjust the rules for sorting and classifying the code by modifying the `singles` and `blocks` dictionaries:

- **Adding New Code Elements:**
  - Define new elements or blocks in the `singles` or `blocks` dictionaries with the necessary parameters.
  
- **Changing Sorting Behavior:**
  - Adjust the `sort` and `keep_position` flags in the `blocks` dictionary to control how blocks are reordered.
 
## Exemple 

### From  
```js
import React from 'react'; 
import Component1 from './Component1';
import Component2 from './Component2';

/*
This is the VictoryList class that manages a list of items
*/
export class VictoryList {
    constructor(items = []) {
        this.items = items;
    }
    /*
    This method adds a new item to the list
    */
    addVictory(item) {
        this.items.push(item);
        if (item === 3) {
            return 2; // Special victory condition
        } else if (item === 5) {
            return 9; // Another special victory condition
        }

        for (let i = 0; i < 5; i++) {
            console.log(i); // Victory parade
        }
    }

    /*
    This method returns the total number of victories
    */
    getTotalVictories() {
        return this.items.length;
    }

    /*
    This method removes the last victory from the list
    */
    removeLastVictory() {
        return this.items.pop();
    }
}

/*
This is the ChampionCalculator class that performs calculations
*/
export class ChampionCalculator {
    constructor(number) {
        this.number = number;
    }

    /*
    This method checks if the number is a champion (even)
    */
    isChampion() {
        return this.number % 2 === 0;
    }

    /*
    This method multiplies the number by a victory factor
    */
    multiplyByFactor(factor) {
        return this.number * factor;
    }

    /*
    This method adds a victory value to the number
    */
    addVictoryPoints(value) {
        return this.number + value;
    }
}

/*
This is the Hero class that handles basic operations
*/

class Hero {
    constructor(name) {
        this.name = name;
    }

    /*
    This method logs a heroic greeting message
    */
    greetHero() {
        console.log(`Greetings, Hero ${this.name}!`);
    }

    /*
    This method returns the length of the hero's name
    */
    getHeroNameLength() {
        return this.name.length;
    }

    /*
    This method converts the hero's name to uppercase
    */
    makeHeroNameUppercase() {
        return this.name.toUpperCase();
    }
}

export default Hero;
```

### To

```js
import React from 'react'; 
import Component1 from './Component1';
import Component2 from './Component2';

/*ELEMENTS NAME SUMMARY
- [class] ChampionCalculator
   - [methods] constructor
   - [methods] addVictoryPoints
   - [methods] isChampion
   - [methods] multiplyByFactor
- [class] Hero
   - [methods] constructor
   - [methods] getHeroNameLength
   - [methods] greetHero
   - [methods] makeHeroNameUppercase
- [class] VictoryList
   - [methods] constructor
   - [methods] addVictory
   - [methods] getTotalVictories
   - [methods] removeLastVictory
*/


/*
This is the ChampionCalculator class that performs calculations
*/
export class ChampionCalculator {
    constructor(number) {
        this.number = number;
    }

    /*
    This method adds a victory value to the number
    */
    addVictoryPoints(value) {
        return this.number + value;
    }

    /*
    This method checks if the number is a champion (even)
    */
    isChampion() {
        return this.number % 2 === 0;
    }

    /*
    This method multiplies the number by a victory factor
    */
    multiplyByFactor(factor) {
        return this.number * factor;
    }

}

/*
This is the Hero class that handles basic operations
*/

class Hero {
    constructor(name) {
        this.name = name;
    }

    /*
    This method returns the length of the hero's name
    */
    getHeroNameLength() {
        return this.name.length;
    }

    /*
    This method logs a heroic greeting message
    */
    greetHero() {
        console.log(`Greetings, Hero ${this.name}!`);
    }

    /*
    This method converts the hero's name to uppercase
    */
    makeHeroNameUppercase() {
        return this.name.toUpperCase();
    }

}

/*
This is the VictoryList class that manages a list of items
*/
export class VictoryList {
    constructor(items = []) {
        this.items = items;
    }

    /*
    This method adds a new item to the list
    */
    addVictory(item) {
        this.items.push(item);
        if (item === 3) {
            return 2; // Special victory condition
        } else if (item === 5) {
            return 9; // Another special victory condition
        }

        for (let i = 0; i < 5; i++) {
            console.log(i); // Victory parade
        }
    }

    /*
    This method returns the total number of victories
    */
    getTotalVictories() {
        return this.items.length;
    }

    /*
    This method removes the last victory from the list
    */
    removeLastVictory() {
        return this.items.pop();
    }

}

export default Hero;
```

## Contribution

If you want to contribute to the development of this program, feel free to submit a pull request or suggest improvements.

## License

This project is open-source and available under the MIT License. 

# NBA Project

This README will provide the overview of the NBA Project within this respository. This project will include web-scraping (from multiple sources), data cleaning, data processing (merging datasets, feature engineering), and the creation of visualizations to generate insights. 


## Table of contents
* [Motivation](#motivation)
* [Objective](#objective)
* [Methodology](#methodology)
  * [Scraping](#scraping)
  * [Cleaning](#cleaning)
  * [Processing](#processing)
* [Analysis](#analysis)
  * [Analysis of Injury Trends](#analysis-of-injury-trends)
  * [Analysis of Other Factors](#analysis-of-other-factors)
* [Conclusion](#conclusion)
* [Additional instructions for using this repository](#additional_instructions_for_using_this_repository)

## Motivation
This project is influenced by article [Injury in the National Basketball Association](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3445097/). The study aims to review injuries and medical conditions affecting National Basketball Association athletes over a 17-year period. 

As an avid basketball fan, I often reflect on past seasons and the injuries experienced by players, which often diminishes a team's main objective: winning a championship. Injuries often have a long-lasting impact, athletes may return to playing basketball, but their style of play has changed, whether its due to fear or suffering another injury or one more sevre, as noted in the article [Fear of Reinjury in Athletes](https://pubmed-ncbi-nlm-nih-gov.ucsf.idm.oclc.org/27590793/)

## Objective
In more recent years, there has been an increase in the injuries suffered throughout the NBA, specifically impacting team dynamics and playoff aspiration. Key players frequently endure serious injuries that necessitate prolonged periods of rehabilitation, disrupting team cohesion and performance.These injuries not only sideline star athletes but also disrupt the strategic balance of teams, affecting their chances of success and playoff contention.

The objective of this project is to determine what injuries occur at specific positions on a NBA team, and while doing so, explore the nature of NBA injuries in during the past decade.

## Methodology
The methodology for this project was influenced by the analysis conducted in the [GitHub Repository](https://github.com/elap733/NBA-Injuries-Analysis.git). This project provided valuable insights for analyzing NBA injuries, which has guided the workflow in this project. 

![WorkFlow](https://cdn.discordapp.com/attachments/1219487952674095134/1219488090926874725/workflow.png?ex=660b7bc9&is=65f906c9&hm=a974904fba025887f591b8ce3ab1b8c44f2028aaf040806f48571175b37e3708&)

The upcoming sections will delve into detailed explanation of how the data was scraped, cleaned, and processed. Please note, the process for scraping, cleaning, and processing the data was heavily influenced by [GitHub Repository](https://github.com/elap733/NBA-Injuries-Analysis.git). However, not all techniques were utilized to avoid excessive resource consumption.

### Scraping

Python's *BeautifulSoup* package was utilized to create four script to scrape data from the following sources:

#### Data Sources 
1. **NBA Injury Data**

  NBA injury data (2013-2023) was scraped from the website [Prosports Transactions](http://prosportstransactions.com/). The site is a Pro Sports Transactions Archive and documents every transaction -- including trades, free agent movements, signings, waivings, draft picks, injuries, movement to and from minor leagues, disciplinary actions, and legal/criminal actions— in the history of five popular North American professional sports (baseball, basketball, football, hockey, and soccer). For the purpose of this project, I focused on two transacation types:
    * **"Missed games due to injury/personal reasons"**
    * This transaction (event) occurs when a player - who is currently on their team's active roster - misses a scheduled game. These missed game events are typically short duration (1-3 games). 
     * **"Movement to/from injured/inactive list (IL)"**
     This transaction (event) occurs when a team places a player on their inactive roster. Teams typically move a player to the inactive roster if the player is expected to be out due to an injury for an extended period of time. This allows another (healthy) player to assume the injured player's spot on the active roster.

      A "transaction" event in this database provides the following information:
   *  'Date' - Date of missed game/ movement to IL 
   *  'Team' - The player's team
   *  'Acquired' - The name of the player returning to lineup
   *  'Relinquished' - The name of the player missing a game or placed on the IL
   *  'Notes' - A description of the event/injury

My scraped injury datasets included more than 17,000 "inactive list events" and more than 9,000 "missed game events.

2. **NBA Schedule Data**

  Team schedules (2013-2023) were scraped from the website [Basketball Reference](http://basketballreference.com/). This data allowed me to:
   * Determine how many games a player actually missed due to injury
   * Determine when the missed game occurred (i.e. the season  -  regular, post, or offseason)

3. **NBA Player Statistics/Bio Data**

  Player statistics (2013-2023) were scraped from the website [Basketball Reference](http://basketballreference.com/). This scraped dataset of more than 9,000 entries allowed me to:
   * Examine correlations between player age, usage (minutes played) and injury events
   * Constrain my analysis to players with a minimum amount of playing time.
     * In this analysis, a threshold of 10 minutes played per game average (i.e. a player must have averaged at least 10 minutes per game during the season in which the injury event occurred).
     * By doing this I was able to focus my analysis on the most relevant segment of the player population - starters and first string reserve players, also known as key players.

[Link to code for data scraping]()

[Link to scraped datasets]()

### Cleaning 

With the scraping of the dataset concluded, it was time to move onto the cleaning portion for this project.

*Cleaning Steps*
- Dropping unnecessary columns
- Dropping rows with missing data
- Formatting injury dates
- Formatting season "name" in a consistent fashion
  - Theory: a season is referred to by the year in which the season started (ex. the 2018/2019 season began in 2018 so its refer to it as the "2018" season)
- Formatting team names in a consistent fashion
  - Consistent team name format was critical for merging/linking datasets.
  - Inconsistencies that needed to be handled:
    - Some datasets used team name abbreviations (e.g. OKC), others used mascots name (e.g. Thunder). 
    - Theory: team name = full city name + mascot (e.g. Oklahoma City Thunder)
    - Several teams have changed names and cities over the past decade. Some, like the Charlotte Hornets, have changed names and cities multiple times. 
- Formatting player names in a consistent fashion
  - Consistent player name format/spelling was also critical for merging/linking datasets. 
  - Inconsistencies that needed to be handled:
    - _Basketball Reference_ uses special characters (accents) - _Prosports Transactions_ does not.
    - _Prosports Transactions_ includes suffixes (Jr., Sr., III) - _Basketball Reference_ does not.
    - Some players have multiple aliases (name spellings) . _Prosports Transactions_ includes all aliases/spellings with each transaction, _Basketball Reference_ uses just a single name spelling for each player.

[Link to code for data cleaning]()

#### Processing 

Now that the data has been cleaned, it is necessary to process the data to prepare for analysis:

*Processing of Player Stats data*:

- For every NBA player, calculate the following for each season in which they played:
  - Total minutes played in prior seasons
  - Total games played in prior seasons

*Processing of NBA Schedules data*:

- For each game, identify the season in which it occurred (regular or post) 
- Calculate the number of back-to-back game sets each season

*Processing of Inactive List* and *Missed Game Events* data:

- For each event, calculate the number games missed due to that event
  - This was the most important, but also most complicated processing step. It required processed NBA schedule data as an additional input.
- Process transaction "notes" to facilitate injury analysis
  - A 'key word' dictionary was used to filter transaction 'notes'. This allowed for events that was due to injury, events due to rest, events due to sickness, event due to other personal reasons (funeral, birth), events due to suspension, etc., can be sorted out. 
  - For events due to actual injury, they were indenfiied by categorizing the injured body part (e.g. shin, ankle, knee, shoulder) and body region (e.g. lower leg, upper leg , torso).

*Merging processed Inactive List / Missed Game Events data with Player Stats data*:

- Merge datasets on "player name" and "year" columns

[Link to code for processing data]()

## Analysis  

This analysis focuses on players averaging more than 10 minutes per game in a given season. 

### Analysis of Injury 
This project will not be the first or the last to utilize [Prosports Transactions](http://prosportstransactions.com/). However, I do think because it uses NBA schedule data and player stats it will be useful to visualize the injuries that occur at specific levels. The merging of the teams schedule and injury data, allows to determine the injury events throughout the year, injury occuring at specific levels, the missed games due to injury, and the specific injuries that occur at specific positions. 

**Fig 1: Count of Injury Events Each Season** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

**Fig 2: Count of Injury Events For Specific Position** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

**Fig 3: Count of Missed Games Due to Injury** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

**Fig 4: Count of Missed Games Due to Injury For Specific Position** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

**Fig 5: Count of Missed Games Due to Specific Injury For Guard Position** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

**Fig 6: Count of Missed Games Due to Specific Injury For Forward Position** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

**Fig 7: Count of Missed Games Due to Specific Injury For Center Position** [Code To Recreate Plot]()

*NOTE: excluded events related to personal reasons, rest, or sickness; included only players averaging 10 minutes per game.*

## Conclusions

The analysis of NBA injuruies (2013-2023 season) revealed an increase of missed games due to injuries have increased in recent years. This project explored the injuries that occur at specific positions and I happy to report the objective of this project has been completed. However, it has also raised other questions of interest, like, does a teams play style impact how many injuries occur in a season? Are key players more likely to be injured because they are the destinated scorer. 

## Additional Instructions For Using This Repository

### Required Packages

[Requirements]()

### Folder Structure

**Data**

- **00** - Uncleaned scraped datasets & scraped code
- **01** - Cleaned datasets & cleaning code
- **02** - Processed datasets & processing code
- **03** - Visualizations & Visualization code

**References**

- **utilities** - Code to create Team Dictionary, Team Abbreviations, and Team Nicknames Dictionaries
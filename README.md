
# ChatBot

This project is the project for the college subject "Artificial Intelligence"


## About

This project contains 3 files:
- knowledge.json
- ChatBot.py
- test-API.py


In the ChatBot.py file is the source code of the bot, where it has the "ability" to answer questions that are stored in the json file, if they are not, it will store the answer if it will be given by the user.

In the test-API.py file we have made it possible for the user to communicate with the bot through the terminal window.

And in the knowledge.json file, here are all the questions and answers stored by the bot.

This project, in short, is a bot that learns from the user, if it doesn't know the answer, it makes you tell it the answer.



## How to Run ChaBot

Clone the project

```bash
  git clone https://github.com/Andrei6700/ChaBot.git
```

Go to the ChaBot  directory

```bash
  cd ChaBot
```

Install dependencies

```bash
  pip install
```

Start 

```bash
  python -u "``path``\ChatBot\ChatBot.py"
```

## How to Run test-API

```bash
  cd ChaBot
```

Start 

```bash
   python -u "`path`\ChatBot\test-API.py"
```

## Features

- Learn from you
- Answer your question
- answer matemathics basic problems


##

```py

    # -----------------0.5-----------------|
    # pune intrebarea :                    |                            
    # Tu: saLuT                            |                    
    # ChatBot: Salut                       |                         
    # Tu: saut                             |                   
    # ChatBot: Salut                       |                         
    # Tu: cae e data                       |                         
    # ChatBot:  salut                      |                           
    # Tu: care e data                      |                          
    # ChatBot:  salut                      |                           
    # Tu: care e ziua                      |                
    # ChatBot: Sincer nu iti stiu numele,..|
    # -------------------------------------|
    # -----------------0.6-----------------|
    # Tu: salt                             |                         
    # ChatBot: Salut                       |                                 
    # Tu: saul                             |
    # ChatBot: Salut                       |
    # Tu: data                             |
    # ChatBot:  salut                      |
    # Tu: care e dati                      |
    # ChatBot: I don't know the answer to..|
    # ChatBot: Te rog să-mi spui răspunsu..|
    # Tu: skip                             |
    # Tu: ce zi e azi ?                    |
    # ChatBot: Pai bine, tu ? Cum mai e v..|
    # -------------------------------------|
    # -----------------0.7-----------------| 
    # Tu: salyt                            |
    # ChatBot: Salut                       |
    # Tu: sult                             |
    # ChatBot: I don't know the answer ... |
    # Tu: skip                             |
    # Tu: data                             |
    # ChatBot: I don't know the answer ... |
    # ChatBot: Te rog să-mi spui răspun... |
    # Tu:                                  |
    # -------------------------------------| 
    # -----------------0.8-----------------| 
    # Tu: salyt                            |
    # ChatBot: Salut                       |
    # Tu: sult                             |
    # ChatBot: I don't know the answer ... |
    # Tu: skip                             |
    # Tu: data                             |
    # ChatBot: I don't know the answer ... |
    # ChatBot: Te rog să-mi spui răspun... |
    # Tu:                                  |
    # -------------------------------------| 
    # -----------------0.9-----------------| 
    # Tu: saut                             |       
    # ChatBot: I don't know the answer t...|
    # ChatBot: Te rog să-mi spui răspuns...|
    # Tu: skip                             |    
    # Tu: salut                            |     
    # ChatBot: Salut                       | 
    # Tu: buna sala                        |
    # ChatBot: I don't know the answer t...|
    # ChatBot: Te rog să-mi spui răspuns...|
    # Tu:
    # -------------------------------------|

```

## Documentation

[Documentation](https://realpython.com/python-ai-neural-network/)
[Documentation](https://www.create-learn.us/blog/how-to-make-ai-in-python-tutorial/)


## Screenshots

![alt text](image.png)

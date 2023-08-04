# The game

## Set up
Needs python 3.X and virtualenv
Dependencies crash at Python 3.10
Project stable at Python 3.8.X

- `Git clone https://github.com/hackupc/thegame.git && cd thegame`
- `virtualenv env --python=python3`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`
- (Optional) If using Postgres, set up the necessary environment variables for its usage before this step
- `python manage.py migrate`

## Features

- Admin page to create Challenges and more .
- Auto HTML templating for Challenges (Image, template, File, Audio, Video, None).
- MyHackUPC login (no passwords managed here).
- Auto admin user for organizers.
- Restriction on hacker submits (max X every 5 minutes).
- Ranking page with local time.
- Challenge stats and user attempts.
- Codes encrypted.
- Troll codes to redirect to urls with ChallengeTroll model.
- Votes and comment for each challenge and custom reactions images with VoteReaction model.

## Usage

### Challenge

- **name:** Challenge title
- **description:** Challenge description (HTML format optional).
- **order:** Challenge phase. User cannot see challenges if not completed all the challenges from previous phase (initial = 1).
- **file:** Challenge file image, video, audio and HTML (django tags can be used).  
- **type:** Challenge type in order to render the file. If set to HTML, his url won't exist making it secret.
- **solution:** Challenge solution. WriteOnly field. Encrypted.
- **activation_date** Challenge activation date (UTC). Won't be accessible to hackers until this date.

### ChallengeTroll

- **challenge:** Challenge to add a troll code.
- **code:** Code that will trigger the redirection.
- **url:** Url to redirect if code was submitted.

### VoteReaction

- **challenge:** Challenge to add this reaction.
- **type:** Reaction can be happy (vote>5) or sad (vote<=5).
- **image:** Image to display when the hacker votes.

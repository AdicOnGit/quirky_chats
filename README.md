# Chat Image Creator

<p align="center">
  <img src="repo_assests/logo.png" alt="Chat Image Creator" width="300" height="300" />
</p>

## Description

This Python script, `chat_section.py`, generates chat images from JSON-formatted chat data. It creates a visual representation of chat conversations in the form of images with chat bubbles, alternating between left and right to differentiate between two participants.

## Features

- Generates images with custom chat bubbles.
- Alternates bubble colors and positions for different speakers.
- Text wrapping and font size adjustments support.
- Overlays chat images on a default background screen image.

## Requirements

- Python 3.x
- Python Imaging Library (PIL) version 9.5.0

## Installation

Ensure Python and PIL are installed. Install PIL via pip:

```bash
pip install Pillow==9.5.0
```

## Usage

1. **Data Preparation**: Format your chat data in a JSON file named `messages.json`. Each message should be an item in a dictionary, representing the conversation sequence.

   **Example JSON Format**:

   ```json
   [
     {
       "Sequence 1": {
         "text_1": "Hey, did you see that new movie that just came out?",
         "text_2": "Yeah, I watched it last night. It was so intense!",
         "text_3": "Oh really? What was it about?",
         "text_4": "Well, it started off as a romantic comedy, but then it turned into a horror film. I was not expecting that!",
         "text_5": "Wait, what? How did that happen?",
         "text_6": "I don't know, one minute they were having a cute picnic and the next minute there were zombies everywhere. It was wild!",
         "text_7": "Haha, that sounds like a rollercoaster of emotions. I need to watch it now!",
         "text_8": "Definitely! Just be prepared for some unexpected twists. Enjoy!"
       },
       "Sequence 2": {
         "text_1": "Hey, have you ever had a really weird dream?",
         "text_2": "Oh, all the time! My dreams are always super bizarre.",
         "text_3": "Well, last night I dreamt that I was being chased by a giant talking banana.",
         "text_4": "What? That's hilarious! Did it catch you?",
         "text_5": "No, thankfully I managed to escape by hiding in a giant bowl of cereal. It was so random!",
         "text_6": "Haha, that's amazing! I wish I had dreams like that. Mine are usually just boring.",
         "text_7": "Trust me, it's not always fun. Sometimes I wake up feeling really confused.",
         "text_8": "I can imagine. Well, I hope you have more entertaining dreams in the future!",
         "text_9": "Thanks, I'll keep you updated if I encounter any more talking fruits!"
       },
       "Sequence 3": {
         "text_1": "Hey, did you hear about that new haunted house attraction in town?",
         "text_2": "Yeah, I heard it's supposed to be really scary. Are you planning to go?",
         "text_3": "I was thinking about it, but then I heard that people have actually gone missing inside.",
         "text_4": "Wait, seriously? That's terrifying!",
         "text_5": "I know, right? I don't think I want to risk it. I'll stick to watching horror movies from the safety of my couch.",
         "text_6": "Good call. I don't think I'm brave enough to enter a potentially dangerous haunted house either.",
         "text_7": "Yeah, I'd rather not become a ghost myself. Let's just enjoy the spooky season in a safer way.",
         "text_8": "Agreed! We can have a scary movie marathon instead. No risk of disappearing into thin air.",
         "text_9": "Sounds like a plan. I'll bring the popcorn and you bring the screams!"
       },
       "Sequence 4": {
         "text_1": "Hey, have you ever had a really embarrassing moment in public?",
         "text_2": "Oh, definitely! I've had my fair share of embarrassing moments.",
         "text_3": "Well, yesterday I was walking down the street and I slipped on a banana peel. It was straight out of a cartoon!",
         "text_4": "No way! Did anyone see?",
         "text_5": "Unfortunately, there were a few people around. I tried to play it cool, but I'm pretty sure they all saw me.",
         "text_6": "Haha, that's rough. At least you didn't break anything, right?",
         "text_7": "Thankfully, no. Just my pride. I'll be more careful around bananas from now on.",
         "text_8": "Lesson learned. Watch out for those sneaky banana peels!",
         "text_9": "Definitely! I don't want to become a walking meme again.",
         "text_10": "Haha, don't worry, I won't let you forget it!"
       },
       "Sequence 5": {
         "text_1": "Hey, have you ever had a really strange encounter with a stranger?",
         "text_2": "Oh, for sure! I've had some pretty weird encounters.",
         "text_3": "Well, yesterday I was waiting for the bus and this random person came up to me and started reciting Shakespeare.",
         "text_4": "No way! That's so random. Did they just walk away after that?",
         "text_5": "Actually, they kept reciting for a good five minutes. It was like being in a live theater performance.",
         "text_6": "Haha, that's both bizarre and impressive. Did they at least do a good job?",
         "text_7": "Surprisingly, they were actually really good! I was low-key impressed by their Shakespearean skills.",
         "text_8": "That's wild. I hope they didn't expect you to join in on the recital.",
         "text_9": "Thankfully, they didn't. I just stood there awkwardly, trying to process what was happening.",
         "text_10": "Well, that's definitely a story to tell. Shakespeare in the streets!",
         "text_11": "Haha, exactly! It was definitely a unique experience."
       }
     }
   ]
   ```

2. **Default Screen Image**: Place a default background image (`default_screen.png`) in the script directory.

3. **Run the Script**: Execute the script with:

   ```bash
   python chat_section.py
   ```

4. **Output**: The script generates a series of PNG images for each chat bubble in the conversation.

## Customization

- Modify `bubble_colors` in `ChatImageCreator` to change bubble colors.
- Adjust `font_size` in `ChatImageCreator` for different text sizes.
- Change `image_size` in `ChatImageCreator` for varying image dimensions.

## Contributing

Contributions are welcome. Fork this repository and submit pull requests with improvements.

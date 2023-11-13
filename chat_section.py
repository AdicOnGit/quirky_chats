from gtts import gTTS
import os
import textwrap
import json
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, VideoFileClip
import tempfile
import numpy as np


class ChatBubble:
    def __init__(self, image_draw, image_size, font):
        self.draw = image_draw
        self.image_size = image_size
        self.font = font
        self.last_position = 150
        self.bubble_padding = 20
        self.bubble_radius = 35
        self.text_color = "#FFFFFF"
        self.bubble_gap = 50

    def draw_bubble(self, text, base_position, fill_color, font_path=None, line_height_factor=1.2):
        max_text_width_ratio = 2.3  # threshold for text wrapping before max bubble width
        max_text_width = int(
            self.image_size[0] / max_text_width_ratio) - 2 * self.bubble_padding
        wrapped_text = textwrap.fill(
            text, width=max_text_width // self.font.getsize(" ")[0])
        lines = wrapped_text.split('\n')
        text_width = max(self.font.getsize(line)[0] for line in lines)
        line_height = self.font.getsize('Ay')[1] * line_height_factor
        text_height = len(lines) * line_height
        bubble_width_limit_ratio = 1.3  # 75% of image width
        bubble_size = (min(text_width + 2 * self.bubble_padding, self.image_size[0] / bubble_width_limit_ratio),
                       text_height + 2 * self.bubble_padding)
        bubble_position_x_left = 20
        bubble_position_x_right = self.image_size[0] - \
            bubble_position_x_left - bubble_size[0]
        position = [bubble_position_x_left, self.last_position] if base_position == 'left' else [
            bubble_position_x_right, self.last_position]
        bubble = [tuple(position), (position[0] + bubble_size[0],
                                    position[1] + bubble_size[1])]
        self.draw.rounded_rectangle(
            bubble, fill=fill_color, outline=None, width=1, radius=self.bubble_radius)
        text_y_position = position[1] + (bubble_size[1] - text_height) / 2

        for i, line in enumerate(lines):
            line_y_position = text_y_position + i * line_height
            self.draw.text((position[0] + self.bubble_padding, line_y_position),
                           line, fill=self.text_color, font=self.font)

        self.last_position += bubble_size[1] + self.bubble_gap
        return bubble_size[1]


class ChatImageCreator:
    def __init__(self, chat_data, image_size=(1240, 1858), font_size=30):
        self.chat_data = chat_data
        self.image_size = image_size
        self.font_size = font_size

    def create_image(self, bubble_heights, key):
        image = Image.new("RGBA", self.image_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = self.load_font(self.font_size)
        bubble_drawer = ChatBubble(draw, self.image_size, font)
        bubble_colors = {"left": "#363638", "right": "#005247"}

        position = "left"
        bubble_heights[key] = {}
        for message_key, message in self.chat_data.items():
            fill_color = bubble_colors[position]
            bubble_height = bubble_drawer.draw_bubble(
                message, position, fill_color)
            bubble_heights[key][message_key] = bubble_height
            position = "right" if position == "left" else "left"

        return image

    def overlay_on_default_screen(self, default_screen_path, top_offset=160, bubble_heights=None, key=None):
        default_screen = Image.open(default_screen_path)
        chat_image = self.create_image(bubble_heights, key)
        x_position = (default_screen.size[0] - self.image_size[0]) // 2
        y_position = top_offset
        default_screen.paste(chat_image, (x_position, y_position), chat_image)
        return default_screen

    def load_font(self, font_size):
        font_path = self.get_font_path()
        try:
            return ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        except IOError:
            return ImageFont.load_default()

    @staticmethod
    def get_font_path():
        windows_font_path = 'C:/Windows/Fonts/Arial.ttf'
        macos_font_path = '/Library/Fonts/Arial.ttf'
        return windows_font_path if os.name == 'nt' else macos_font_path


def t2s_in_memory(chat_texts):
    audio_paths = {}
    for index, (key, text) in enumerate(chat_texts.items()):
        tts = gTTS(text=text, lang='en')
        # Create a temporary file for each audio clip
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            audio_paths[index] = temp_audio.name
    return audio_paths


def crop_and_save_in_memory(final_image, bubble_heights, key):
    image_width = 1240
    last_cropped_height = 0
    gap_between_bubbles = 50
    fixed_height_to_crop_first_two_bubbles = 315
    already_processed_first_image = False
    current_sequence = bubble_heights[key]
    keys = list(current_sequence.keys())
    cropped_images = []
    for i in range(5):
        if not already_processed_first_image:
            new_height_to_crop = current_sequence[keys[i]]
            last_cropped_height = fixed_height_to_crop_first_two_bubbles + new_height_to_crop
            coordinates = (0, 0, image_width, last_cropped_height)
            already_processed_first_image = True
        else:
            last_cropped_height -= current_sequence[keys[i-1]]
            new_height_to_crop = current_sequence[keys[i-1]] + \
                current_sequence[keys[i]]+gap_between_bubbles
            coordinates = (0, last_cropped_height, image_width,
                           last_cropped_height + new_height_to_crop)
            last_cropped_height += new_height_to_crop
        cropped_img = final_image.crop(coordinates)
        cropped_images.append(cropped_img)
    return cropped_images


def overlay_images_on_video_in_memory(image_clips, audio_streams, video_path, output_path):
    clips = []
    total_duration = 0

    # Load the base video to get its size and aspect ratio
    video_clip = VideoFileClip(video_path)
    video_size = video_clip.size

    for seq_key in sorted(image_clips.keys()):
        images = image_clips[seq_key]
        audios = audio_streams[seq_key]

        # Create clips for each image and audio pair
        for i, image in enumerate(images):
            if i in audios:
                audio_file_path = audios[i]
                audio_clip = AudioFileClip(audio_file_path, fps=22050)
                total_duration += audio_clip.duration

                # Convert PIL Image to NumPy array
                np_image = np.array(image.convert('RGB'))

                # Load image as NumPy array and resize if necessary
                image_clip = ImageClip(np_image)

                # Resize image to fit video's width while maintaining aspect ratio, if it's wider than the video
                if image_clip.size[0] > video_size[0]:
                    aspect_ratio = image_clip.size[0] / image_clip.size[1]
                    new_height = int(video_size[0] / aspect_ratio)
                    image_clip = image_clip.resize(
                        width=video_size[0], height=new_height)

                # Set the duration of the image clip to match the audio clip
                image_clip = image_clip.set_duration(audio_clip.duration)

                # Create a clip with the image centered in the video frame
                final_clip = CompositeVideoClip(
                    [image_clip.set_position("center")], size=video_size)
                final_clip = final_clip.set_audio(audio_clip)
                clips.append(final_clip)

    # Concatenate all clips and set the size to match the background video
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = CompositeVideoClip(
        [video_clip, final_video.set_position("center")], size=video_size)
    final_video = final_video.subclip(0, total_duration)
    final_video.write_videofile(
        output_path, codec='libx264', audio_codec='aac')


def main():
    default_screen_path = "default/default_screen.png"
    video_path = "default/default_video.mp4"
    output_path = "output/final_video.mp4"

    with open("messages.json", "r") as f:
        conversation_list = json.load(f)
        current_video = conversation_list[-1]

        # Create dictionaries to store in-memory images and audio streams
        in_memory_images = {}
        in_memory_audio = {}

        for key, sequence in current_video.items():
            chat_image_creator = ChatImageCreator(sequence, font_size=50)

            # Initialize bubble_heights as an empty dictionary
            bubble_heights = {}

            final_image = chat_image_creator.overlay_on_default_screen(
                default_screen_path, bubble_heights=bubble_heights, key=key
            )
            cropped_images = crop_and_save_in_memory(
                final_image, bubble_heights, key)
            audio_streams = t2s_in_memory(sequence)

            in_memory_images[key] = cropped_images
            in_memory_audio[key] = audio_streams

        overlay_images_on_video_in_memory(
            in_memory_images, in_memory_audio, video_path, output_path)

        # Cleanup temporary audio files
        for seq_audios in in_memory_audio.values():
            for audio_path in seq_audios.values():
                if os.path.exists(audio_path):
                    os.remove(audio_path)


if __name__ == "__main__":
    main()


''' TO DOs:
1. Put them in one class called "VideoCreator"
2. I wanna add a background audio to the video with custom volume.
3. I wanna put a message received sound when left bubble narration starts and a message sent sound when right bubble narration finishes to give an impression of message sent and received in real world.
4. The message received sound, sent and background sound will be provided by me.
Do you understand my query ? How do you think I wanna implement the sounds on the messages
'''

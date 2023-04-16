import json

def convert_json_to_srt(json_file_path, srt_file_path):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
    
    with open(srt_file_path, 'w') as srt_file:
        for i, item in enumerate(data):
            start_time = item['start_sec']
            end_time = item['end_sec']
            text = item['target']
            
            srt_file.write(str(i + 1) + '\n')
            srt_file.write(format_time(start_time) + ' --> ' + format_time(end_time) + '\n')
            srt_file.write(text + '\n\n')

def format_time(seconds):
    # Format time in seconds to SRT format (hh:mm:ss,milliseconds)
    milliseconds = int(seconds % 1 * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, milliseconds)

# Example usage:
convert_json_to_srt('caption.json', 'caption.srt')

def format_srt(srt_path, max_chars_per_line=30):
    with open(srt_path, 'r') as srt_file:
        srt_text = srt_file.read()

    # Replace any \r\n line endings with just \n
    srt_text = srt_text.replace('\r\n', '\n')

    # Split the text into individual subtitle blocks
    subtitle_blocks = srt_text.strip().split('\n\n')

    # Format subtitle text to be easier to read
    formatted_srt = ''
    for subtitle_block in subtitle_blocks:
        subtitle_lines = subtitle_block.strip().split('\n')
        subtitle_text = subtitle_lines[2]

        # Break subtitle text into multiple lines if it's too long
        words = subtitle_text.split()
        new_lines = []
        current_line = ''
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars_per_line:
                current_line += ' ' + word
            else:
                new_lines.append(current_line.strip())
                current_line = word
        new_lines.append(current_line.strip())
        subtitle_text = '\n'.join(new_lines)

        # Add formatted subtitle block to output string
        formatted_srt += f'{subtitle_lines[0]}\n'
        formatted_srt += f'{subtitle_lines[1]}\n'
        formatted_srt += f'{subtitle_text}\n\n'

    return formatted_srt
formatted_srt = format_srt('caption.srt', max_chars_per_line=30)
with open('caption.srt', 'w') as f:
    f.write(formatted_srt)

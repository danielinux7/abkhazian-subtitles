#!/bin/bash
SERIE=4
ffmpeg -i video.mp4 -i $SERIE"_ab.m4a" -i $SERIE"_tr.m4a" -i $SERIE"_ru.srt" -i $SERIE"_ab.srt" -i $SERIE"_tr.srt" -i $SERIE"_en.srt" -map 0 -map 1 -map 2 -map 3 -map 4 -map 5 -map 6 -c copy -disposition:a:0 default -metadata:s:a:0 language=abk -metadata:s:a:1 language=tur -c:s mov_text -disposition:s:0 default -metadata:s:s:0 language=rus -metadata:s:s:1 language=abk -metadata:s:s:2 language=tur -metadata:s:s:3 language=eng video_out.mp4


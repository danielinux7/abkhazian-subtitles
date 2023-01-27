for file in $( ls | grep -o "[0-9]*"); 
  do 
    ffmpeg -i $file -c:a copy $file.mp4; 
    mv $file.mp4 $file; 
  done

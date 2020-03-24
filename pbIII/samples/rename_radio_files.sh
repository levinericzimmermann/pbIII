# renaming and normalizing all audio files

for dir in radio/*
do
    i=0
    for f in $dir/*.wav
    do
        sox --norm=-2 "$f" tmp.wav
        rm "$f"
        mv tmp.wav "$dir/$i.wav"
        i=$(( i + 1 ))
    done
done

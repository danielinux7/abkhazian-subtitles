grep '^[0-9]:[0-9][0-9]:.*[0-9]$' caption.sbv | sed -r 's/^(.*),.*$/\1/g' > starttime.txt
grep '^[0-9]:[0-9][0-9]:.*[0-9]$' caption.sbv | sed -r 's/^.*,(.*)$/\1/g' > endtime.txt
grep -v '^[0-9]:[0-9][0-9]:.*[0-9]$' caption.sbv | sed -z -r 's/\n\n/empty/g' | sed -z -r 's/\n/ /g' | sed -z -r 's/empty/\n/g' > text.txt
echo -e "0:00:00.000\t0:00:20.000\t...АУАДА АБЖЬЫ..." > noise.tsv 
echo -e "0:00:00.000\t0:00:20.000\t...АУАДА АБЖЬЫ..." >> noise.tsv 
paste starttime.txt endtime.txt text.txt > caption2.tsv
cat noise.tsv caption2.tsv > caption.tsv
rm starttime.txt endtime.txt text.txt caption2.tsv noise.tsv

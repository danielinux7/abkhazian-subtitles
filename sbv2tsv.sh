#sed -r '/^[0-9]+[\r\n]/d' caption.srt > caption.sbv
#sed -i -r 's/([0-9]+:[0-9]+:[0-9]+),([0-9]+)/\1.\2/g' caption.sbv
#sed -i -r 's/([0-9]+:[0-9]+:[0-9]+\.[0-9]+) --> ([0-9]+:[0-9]+:[0-9]+\.[0-9]+)/\1,\2/g' caption.sbv
grep '^[0-9]:[0-9][0-9]:.*[0-9]$' caption.sbv | sed -r 's/^(.*),.*$/\1/g' > starttime.txt
grep '^[0-9]:[0-9][0-9]:.*[0-9]$' caption.sbv | sed -r 's/^.*,(.*)$/\1/g' > endtime.txt
grep -v '^[0-9]:[0-9][0-9]:.*[0-9]$' caption.sbv | sed -z -r 's/\n\n/empty/g' | sed -z -r 's/\n/ /g' | sed -z -r 's/empty/\n/g' > text.txt
paste starttime.txt endtime.txt text.txt > caption.tsv
rm starttime.txt endtime.txt text.txt

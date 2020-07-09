tail -n +2 cves.csv | split -l 10000 - cves_ -d
for file in cves_*
do
    head -n 1 cves.csv > tmp_file
    cat "$file" >> tmp_file
    mv -f tmp_file "$file"
done
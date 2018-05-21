#set terminal pdf dashed enhanced size 3.5in,2in
set terminal tikz size 5in,2in
set output "data/eval-app.tex"

set style data histogram
set style histogram cluster gap 1.5
set boxwidth 0.7

set auto x
set yrange [0:*]
set grid y
set ylabel "Running time (seconds)"
set ytics scale 0.5,0 nomirror
set xtics scale 0,0
set key inside right spacing 1.75
set style fill solid 1 border rgb "black"

plot "data/app.data" \
        using ($2):xtic(1) title col lc rgb '#ff0101' lt 1, \
     '' using ($3):xtic(1) title col lc rgb '#599bfc' lt 1, \
     '' using ($4):xtic(1) title col lc rgb '#ffb3b3' lt 1, \
     '' using ($5):xtic(1) title col lc rgb '#d3dff2' lt 1

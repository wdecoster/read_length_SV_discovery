for i in *.pr; do
 var=$(echo $i | cut -f2 -d '-' | cut -f1 -d'.') ;
 prec=$(grep ^Prec $i | cut -f2 -d ' ' | sed s/%//) ;
 rec=$(grep ^Rec $i | cut -f2 -d ' ' | sed s/%//) ;
 echo "sniffles" $var $prec $rec "1" | tr ' ' '\t' >> summary.txt ;

done

[ $# -ge 1 ] && date=$1 || date=`date -d "1 days ago" +%Y%m%d`
#readonly rp_hadoop="/home/work/bin/hadoop-client-rp-product/hadoop/bin/hadoop"
i=1;n=30
while [ $i -le $n ]
do
	d=`date -d "${i} days ago $date" +%Y%m%d`
	echo "[`date "+%Y-%m-%d %H:%M:%S"`] �� $i �� ($d)"
	sh start.sh $d
	[ $? -ne 0 ] && { echo "[`date "+%Y-%m-%d %H:%M:%S"`] �� $i �� ($d) ִ��ʧ��...";exit -1; } || { echo "[`date "+%Y-%m-%d %H:%M:%S"`] �� $i ��( $d ) ִ�гɹ�...";  }
    ((i++))
done

#!/bin/bash
# -*- coding: utf-8 -*-

#===============================================================================
#            File:  build.sh
#           Usage:  sh build.sh
#     Description:  �ִ�л���������Ŀ¼��ɾ���ļ����޸�Ȩ��
#    LastModified:  
#         Created:  2014-3-19 16:17 PM CST
# 
#          AUTHOR:  warren@autonavi.com)
#         COMPANY:  autonavi Inc
#         VERSION:  1.0
#            NOTE:  
#           input:  
#          output:  
#===============================================================================


readonly LogDayCnt=90	#��־���������
readonly BakDayCnt=20	#���뱸�ݵ�����
readonly DataDayCnt=7	#���ݱ��ݵ�����

ShellDir=`pwd`
cd $ShellDir

#����shell�ļ��Ŀ�ִ��Ȩ��
#for file in `ls ${ShellDir}/*.sh ${ShellDir}/conf/*.sh`
#do
#        [ ! -x $file ] && chmod a+x $file
#done

readonly RootDir=${ShellDir%/*}
readonly now=`date "+%Y%m%d"`
readonly BakDir=${RootDir}/bak/$now
readonly LogDir=${RootDir}/log/$now
readonly DataDir=${RootDir}/data/$now

#����Ŀ¼
file_dir=( $BakDir $LogDir $DataDir )
index=$((${#file_dir[*]}-1))
for i in `seq 0 $index`
do
        [ ! -d ${file_dir[$i]} ] && mkdir -p ${file_dir[$i]}
done

#ɾ�����ڵı���
#for i in `seq 0 $index`
#do
#	find ${BakDir%/*} -maxdepth 1 -mindepth 1 -mtime +${BakDayCnt} -exec rm \-rf {} \; -print
#done

#����,ʱ�������
cp -ru ./* ${BakDir}/

find ${BakDir%/*} -maxdepth 1 -mindepth 1 -mtime +${BakDayCnt} -exec rm \-rf {} \; -print
find ${LogDir%/*} -maxdepth 1 -mindepth 1 -mtime +$LogDayCnt -exec rm \-rf {} \; -print
find ${DataDir%/*} -maxdepth 1 -mindepth 1 -mtime +$DataDayCnt -exec rm \-rf {} \; -print


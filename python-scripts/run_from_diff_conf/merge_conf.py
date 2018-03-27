#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import csv
import os
import shutil
import subprocess
import time
import sys

etcd_host = '1.1.1.1'
etcd_port = '8004'
etcd_root = '/URI'
etcd_gid = '105'
merge_tools_path ='./'
#etcd gm dir info
#print base_gm_url
out_conf_dir = os.path.join(merge_tools_path + 'confd/')
base_gm_url = "http://%s:%s/v2/keys%s/%s/" % (etcd_host, etcd_port, etcd_root, etcd_gid)
def get_gm_data_info(shard_id):
    redis_host = requests.get(url=base_gm_url+'%s/gm/redis' % shard_id).json()['node']['value']
    redis_num = requests.get(url=base_gm_url+'%s/gm/redis_db' % shard_id).json()['node']['value']
    rank_host = requests.get(url=base_gm_url+'%s/gm/redis_rank' % shard_id).json()['node']['value']
    rank_num = requests.get(url=base_gm_url+'%s/gm/redis_rank_db' % shard_id).json()['node']['value']
    #print each_shard, redis_host, redis_num, rank_host, rank_num
    return redis_host, redis_num, rank_host, rank_num
def create_conf(out_conf_dir, etcd_host, etcd_port, etcd_root, etcd_gid, Ashard, Aredis_db, Aredis_num, Arank_db, Arank_num, Bshard, Bredis_db, Bredis_num, Brank_db, Brank_num, Rshard, Rredis_db, Rredis_num, Rrank_db, Rrank_num):
    conf_name = out_conf_dir + '/' + Ashard + '_' + Bshard + '_merge.toml'
    with open(conf_name, 'w') as f2:
        f2.write('[MergeCfg]' + '\n'*2)
        f2.write('etcd_endpoint = ["http://%s:%s"]' % (etcd_host, etcd_port) + '\n')
        f2.write('etcd_root = "%s"' % etcd_root + '\n')
        f2.write('output_path = "/opt/supervisor/log"' + '\n'*2)
        f2.write('Gid=%s' % etcd_gid + '\n'*2)
        f2.write('ARedis="%s"' % Aredis_db + '\n')
        f2.write('ARedisDB=%s' % Aredis_num + '\n')
        f2.write('ARedisDBAuth="mUEiGo1Vy1bZeFhVsPN3VKnV"' + '\n')
        f2.write('ARedisRank="%s"' % Arank_db + '\n')
        f2.write('ARedisRankDB=%s' % Arank_num + '\n')
        f2.write('ARedisRankDBAuth="mUEiGo1Vy1bZeFhVsPN3VKnV"' + '\n')
        f2.write('AShardId=%s' % Ashard + '\n'*2)
        f2.write('BRedis="%s"' % Bredis_db + '\n')
        f2.write('BRedisDB=%s' % Bredis_num + '\n')
        f2.write('BRedisDBAuth="mUEiGo1Vy1bZeFhVsPN3VKnV"' + '\n')
        f2.write('BRedisRank="%s"' % Brank_db + '\n')
        f2.write('BRedisRankDB=%s' % Brank_num + '\n')
        f2.write('BRedisRankDBAuth="mUEiGo1Vy1bZeFhVsPN3VKnV"' + '\n')
        f2.write('BShardId=%s' % Bshard + '\n'*2)
        f2.write('ResRedis="%s"' % Rredis_db + '\n')
        f2.write('ResRedisDB=%s' % Rredis_num + '\n')
        f2.write('ResRedisDBAuth="mUEiGo1Vy1bZeFhVsPN3VKnV"' + '\n')
        f2.write('ResRedisRank="%s"' % Rrank_db + '\n')
        f2.write('ResRedisRankDB=%s' % Rrank_num + '\n')
        f2.write('ResRedisRankDBAuth="mUEiGo1Vy1bZeFhVsPN3VKnV"' + '\n')
        f2.write('ResShardId=%s' % Rshard + '\n'*2)
        f2.write('DelAccountCorpLvl=30' + '\n') # 角色多级之下，可能删除， 要求30
        f2.write('DelAccountNotLoginMin=10080' + '\n') # 角色多少分钟未登录，可能删除，要求7天=10080，方便qa测试是用p.LogoutTime+p.DebugAbsoluteTime
    f2.close()
def create_conf_file():
    with open('merge_plan.csv', 'rb') as f1:
        f1_csv = csv.reader(f1)
        title = next(f1_csv)
        #print title
        if not os.path.exists(out_conf_dir):
            os.makedirs(out_conf_dir)
        else:
            shutil.rmtree(out_conf_dir)
            os.makedirs(out_conf_dir)
        for each_row in f1_csv:
            #print each_row
            shardA_info = get_gm_data_info(each_row[0])
            shardB_info = get_gm_data_info(each_row[1])
            #print each_row[0],shardA_info,each_row[1],shardB_info
            Ashard = each_row[0]
            Aredis_db = shardA_info[0]
            Aredis_num = shardA_info[1]
            Arank_db = shardA_info[2]
            Arank_num = shardA_info[3]
            Bshard = each_row[1]
            Bredis_db = shardB_info[0]
            Bredis_num = shardB_info[1]
            Brank_db = shardB_info[2]
            Brank_num = shardB_info[3]
            Rshard = each_row[2]
            Rredis_db = each_row[3]
            Rredis_num = each_row[4]
            Rrank_db = each_row[5]
            Rrank_num = each_row[6]
            #print Ashard, Aredis_db, Aredis_num, Arank_db, Arank_num
            #print Bshard, Bredis_db, Bredis_num, Brank_db, Brank_num
            #print Rshard, Rredis_db, Rredis_num, Rrank_db, Rrank_num
            create_conf(out_conf_dir, etcd_host, etcd_port, etcd_root, etcd_gid, Ashard, Aredis_db, Aredis_num, Arank_db,
                        Arank_num, Bshard, Bredis_db, Bredis_num, Brank_db, Brank_num, Rshard, Rredis_db, Rredis_num,
                        Rrank_db, Rrank_num)
def write_log(log_name,log_content):
    log_dir = os.path.join(merge_tools_path + 'log/' + time.strftime("%Y-%m-%d", time.localtime()))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    #print 'I am for debug in Function %s' % sys._getframe().f_code.co_name
    with open(log_dir + '/%s' % log_name, 'w') as f3:
        f3.write(log_content)
    f3.close()

def run_merge_tools():
    if not os.path.isfile('./gamex_merge'):
        print "Merge tools is not exist ! Please check your path now"
        exit(7)
    for each_conf in os.listdir(out_conf_dir):
        try:
            print time.asctime( time.localtime(time.time()) )
            out_bytes = subprocess.check_output(['./gamex_merge', 'allinone', '-c', each_conf],stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            out_bytes = e.output
            code = e.returncode
        print os.path.splitext(each_conf)[0], 'have Done !'
        write_log(os.path.splitext(each_conf)[0] + '.log', out_bytes)

if __name__ == '__main__':
    # create_conf_file()
    run_merge_tools()

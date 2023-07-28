#学计算机哪有不疯的哈哈哈
#别烦我QAQ紫砂了真的QAQ你~干~嘛~~~哎~呦~
#SuperPower文件备份jo本！保存你的美
#11451419........
import os
import configparser
import argparse
import datetime     #获取时间
import qiniu
from qiniu import Auth, put_file
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

#===============函数区域================#
def qiniu_start(_Path_):
    '''qiniu备份启动'''

    if _Path_.endswith('/'):  #如果是目录,取最后一级目录作名字
        tmp = _Path_
        tmp = tmp[:-1]
        pre_filename = os.path.split(tmp)[1]
        filename = getFilename(pre_filename)    #取得压缩包文件名
        ziportar(_Path_,filename)
        Qiniu.gettooken()
        Qiniu.setbackupPath(filename)
        Qiniu.upload_start()
    else:
        path,pre_filename = os.path.split(_Path_)
        path = path + '/'
        filename = getFilename(pre_filename)    #取得压缩包文件名
        ziportar(_Path_,filename)
        Qiniu.gettooken()
        Qiniu.setbackupPath(filename)
        Qiniu.upload_start()

def tx_start(_Path_):
    '''TX备份启动'''

    if _Path_.endswith('/'):  #如果是目录,取最后一级目录作名字
        tmp = _Path_
        tmp = tmp[:-1]
        pre_filename = os.path.split(tmp)[1]
        filename = getFilename(pre_filename)    #取得压缩包文件名
        ziportar(_Path_,filename)
        TX.setbackupPath(filename)
        TX.upload_start()
    else:
        path,pre_filename = os.path.split(_Path_)
        path = path + '/'
        filename = getFilename(pre_filename)    #取得压缩包文件名
        ziportar(_Path_,filename)
        TX.setbackupPath(filename)
        TX.upload_start()

def ziportar(path,filename):    #filename 压缩后文件名
    '''压缩文件,Windows系统zip,Linux系统tar'''
    if path[-1] == '/':
        os.chdir(path)
        os.chdir("../")
        pre_filename = os.path.split(path)[0]
        pre_filename = os.path.split(pre_filename)[1]
    else:
        tmp,pre_filename = os.path.split(args.p)
        os.chdir(tmp)
        pre_filename = os.path.split(path)[1]
    if os.name == 'nt':             
        if path.endswith('/'):      #zip备份整个目录要加*通配符
            pre_filename = pre_filename + '/*'
        os.system("zip " + filename +' '+ pre_filename)
    else:
        os.system("tar -czvf " + filename + pre_filename)
    
def getFilename(pre_filename):
    '''生成带时间戳的压缩包文件名'''
    current_time = datetime.datetime.now()
    filename= pre_filename + f"_{current_time.strftime('%Y%m%d_%H%M%S')}"
    if os.name == 'nt':
        filename = filename + '.zip'
    else:
        filename = filename + '.tar.gz'
    return filename



#======================================#

#=============================定义区域=========================================#

conf_path = "config.conf"
data_test = {       
        "access_key":"",
        "secret_key":"",
        "bucket_name":"",
        "bucket_domain":"",
        "backup_path":""
    }

config = configparser.ConfigParser()    #conf文件解析对象

parser = argparse.ArgumentParser()      #命令行参数对象
parser.add_argument('-uses',type=str,help="指定备份到哪个云存储(默认qiniu)")     
parser.add_argument('-show',action='store_true',help="显示--use可用的内容")
parser.add_argument('-add',type=str,help="添加或修改云存储到conf文件中,请传入名称")
parser.add_argument('-ak',type=str,help="云存储AccessKey")
parser.add_argument('-sk',type=str,help="云存储SecretKey")
parser.add_argument('-bucket',type=str,help="云存储bucket")
parser.add_argument('-region',type=str,help="腾讯COS存储桶所属地域")
parser.add_argument('-backpath',type=str,default="supack_up/",help="云存储路径默认'supack_up/'")
parser.add_argument('-i',action='store_true',help="不使用配置文件中的内容")
parser.add_argument('-p',type=str,help="备份指定目录或该目录下的某一文件")
args = parser.parse_args()

#===========================================================================#

#===========================类区==========================================#
class QiniuYun:
    '''七牛云连接对象'''
    _auth = None     
    _bucket_name = None     #存储空间名称
    _backup_path = None     #备份到云上的路径
    _tooken = None
    _filename = None
    def authorize(self,AK,SK):       
        '''获取七牛AUTH对象'''
        return Auth(AK,SK)

    def gettooken(self):    #要在上传前先调用
        self._tooken = self._auth.upload_token(self._bucket_name)

    def setbackupPath(self,filename):   #要在上传前先调用
        '''传入filename,压缩包的名字'''
        self._filename = filename
        if self._backup_path[:1] == "/":
            self._backup_path = self._backup_path[1:]
        if not self._backup_path.endswith('/'):
            self._backup_path = self._backup_path + '/'
        self._backup_path = self._backup_path + filename


    def upload_start(self):     #开始上传
        '''开始上传'''
        _file = os.getcwd()+'/'+self._filename

        response = put_file(self._tooken,self._backup_path,_file,check_crc=True)
        os.remove(_file)    #删除本地留下的压缩包
        print(response)

    def __init__(self,access_key,secret_key,bucket_name,bkpath):
        self._auth = self.authorize(access_key,secret_key)
        self._bucket_name = bucket_name
        self._backup_path = bkpath



class Txcos:
    '''腾讯COS连接对象'''
    from qcloud_cos import CosConfig
    from qcloud_cos import CosS3Client
    _config = None
    _client = None
    _backup_path = None
    _filename = None
    _bucket_name = None
    def setbackupPath(self,filename):   #要在上传前先调用
        '''传入filename,压缩包的名字'''
        self._filename = filename
        if self._backup_path[:1] == "/":
            self._backup_path = self._backup_path[1:]
        if not self._backup_path.endswith('/'):
            self._backup_path = self._backup_path + '/'
        self._backup_path = self._backup_path + filename
    def upload_start(self):
        '''开始上传'''
        _file = os.getcwd()+'/'+self._filename
        response = self._client.upload_file(
            Bucket=self._bucket_name,
            LocalFilePath=_file,
            Key=self._filename,
            PartSize=1,
            MAXThread=10,
            EnableMD5=False
        )
        os.remove(_file)    #删除本地留下的压缩包
        print(response)
    def __init__(self,access_key,secret_key,bucket_name,bkpath,region,token):
        #临时密钥需要token  其他传None就行
        self._bucket_name = bucket_name
        self._backup_path = bkpath
        self._config = CosConfig(Region=region,SecretId=access_key, SecretKey=secret_key, Token=token, Scheme='https')
        self._client = CosS3Client(self._config)

#===========================================================================#

#===========================主代码==========================================#

if args.i:      
    if not args.p:
        print("-p路径呢？？？？我怎么知道你要传什么")
    else:
        if not args.uses:
            if not args.ak or not args.sk or not args.bucket:
                print("无法连接到七牛云:参数缺失")
                exit()
            Qiniu = QiniuYun(args.ak,args.sk,args.bucket,args.backpath)
            qiniu_start(args.p)
        else:   
            if not args.ak or not args.sk or not args.bucket or not args.region:
                print("无法连接到腾讯COS:参数缺失")
                exit()
            TX = Txcos(args.ak,args.sk,args.bucket,args.backpath,args.region,None)
            tx_start(args.p)

else:    
    if args.add:
        if not os.path.exists(conf_path):
            with open(conf_path,'w') as file:
                pass
        config.read(conf_path)
        if not config.has_section(args.add):    #节是否存在，修改还是添加
            config[args.add] = {
                'AccessKey': args.ak if args.ak else "",
                'SecretKey': args.sk if args.sk else "",
                'bucket': args.bucket if args.bucket else "",
                'backup_path': args.backpath if args.backpath else "",
            }
        else:
            if args.ak:config.set(args.add,'AccessKey',args.ak)
            if args.sk:config.set(args.add,'SecretKey',args.sk)
            if args.bucket:config.set(args.add,'bucket',args.bucket)
            if args.backpath:config.set(args.add,'backup_path',args.backpath)
        with open(conf_path,'w') as configfile:     #'a'模式追加写入'w'模式覆盖写入
            config.write(configfile)   
        if args.p:
            if args.add == "qiniu":
                if not args.ak or not args.sk or not args.bucket:
                    print("无法连接到七牛云")
                    exit()
                Qiniu = QiniuYun(args.ak,args.sk,args.bucket,args.backpath)
                qiniu_start(args.p)               
    if args.uses:    
        if not args.p:
            print("未指定路径")
        else:
            if not os.path.exists(conf_path):
                print("未检测到conf文件,给老子爬去-i或者加上-add啊！！！")
                exit()
            else:
                config.read(conf_path)
                if config.has_section(args.uses):
                    if args.uses == "qiniu":
                        Qiniu = QiniuYun(config.get(args.uses,'accesskey'),config.get(args.uses,'secretkey'),config.get(args.uses,'bucket'),config.get(args.uses,'backup_path'))
                        qiniu_start(args.p)
                    if args.uses == "txCos":    
                        TX = Txcos(config.get(args.uses,'accesskey'),config.get(args.uses,'secretkey'),config.get(args.uses,'bucket'),config.get(args.uses,'backup_path'),config.get(args.uses,'region'),None)
                        tx_start(args.p)
                else:
                    print("未找到服务")

#===========================================================================#
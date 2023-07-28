# Supack
腾讯Cos以及七牛云备份Python脚本
optional arguments:
  -h, --help          show this help message and exit
  -uses USES          指定备份到哪个云存储(默认qiniu)
  -show               显示--use可用的内容
  -add ADD            添加或修改云存储到conf文件中,请传入名称
  -ak AK              云存储AccessKey
  -sk SK              云存储SecretKey
  -bucket BUCKET      云存储bucket
  -region REGION      腾讯COS存储桶所属地域
  -backpath BACKPATH  云存储路径默认'supack_up/'
  -i                  不使用配置文件中的内容
  -p P                备份指定目录或该目录下的某一文件

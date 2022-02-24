# _*_ coding:utf8 _*_
# python2
import arcpy
import sys

# 控制命令窗口传参
param = sys.argv[1]
name = sys.argv[2]

arcpy.env.overwriteOutput = True
arcpy.env.workspace = param
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(str(name)+'_cun_rk.prj')


def dissolve_1():
    '''
    根据xzqdm字段对***_cun_rk.shp进行融合，确保每一个村都是唯一的，并重新计算村人口
    '''
    arcpy.Dissolve_management(str(name)+'_cun_rk.shp',str(name)+'_cun_rk_dissolve',['XZQDM'],[['CZCOUNT','FIRST'],['XZQMC','FIRST']])
    print('数据融合完毕!'.decode('utf-8'))


def addField_Calcul_2():
    '''
    对***_cun_rk_dissolve.shp添加AREA字段，并进行村面积计算
    '''
    arcpy.AddField_management(str(name)+'_cun_rk_dissolve.dbf','AREA','DOUBLE')
    arcpy.CalculateField_management(str(name)+'_cun_rk_dissolve.dbf','AREA','!shape.geodesicArea@METERS!','PYTHON_9.3')
    print('面积字段添加并计算完毕!'.decode('utf-8'))


def spacejoin_3():
    '''
    将***_jiequ.shp与***_cun_rk_dissolve.shp进行空间连接，以获得每个街区所对应的村编码
    '''
    arcpy.SpatialJoin_analysis(str(name)+'_jiequ.shp',str(name)+'_cun_rk_dissolve.shp',str(name)+'_cun_jiequ_spacejoin.shp',match_option='WITHIN')
    print('获取街区所对应的村编码!!!'.decode('utf-8'))


def exportTable_4():
    '''
    将获取每个街区所对应的村编码数据即***_cun_jiequ_spacejoin.shp的相关属性保存为txt文件
    '''
    txt = open(str(name)+'_cun_jiequ_spacejoin.txt','w')
    txt.write('XZQDM'+','+'JIEQU_AREA'+','+'CUN_AREA'+','+'CUN_RK'+'\n')
    rows = arcpy.SearchCursor(str(name)+'_cun_jiequ_spacejoin.shp',fields='XZQDM;Shape_Area;AREA;FIRST_CZCO')
    for row in rows:
        context = str(row.getValue('XZQDM'))+','+str(row.getValue('Shape_Area'))+','+str(row.getValue('AREA'))+','+str(row.getValue('FIRST_CZCO'))+'\n'
        txt.write(context)
    print('空间连接文件创建完毕!!!'.decode('utf-8'))

# 执行所有函数
def execute():
    dissolve_1()
    addField_Calcul_2()
    spacejoin_3()
    exportTable_4()

execute()
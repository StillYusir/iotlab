'''
清洗数据
清洗wishArea
sample = '3205832-3205833'
'''
def CleanWishArea(wishArea):
    tmp = wishArea.split("-")
    for item in tmp:
        if len(item) != 7:
            tmp.remove(item)
    return tmp
'''
清洗wishJobType
sample = "211101 - 211202 - 211401"
'''
def CleanWishJobType(wishJobType):
    tmp = wishJobType.split("-")
    # print(tmp)
    for item in tmp:
        if len(item)!=6:
            tmp.remove(item)
    return tmp



#TODO 建立输入数据与PropertiesMapper之间的映射，例如workerYear=12 ==> workYearMapper[3]

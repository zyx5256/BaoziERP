class Buttoms:
    ADD_TO_INVENTORY = "入库"
    REMOVE_FROM_INVENTORY = "出库"
    CALCULATE = "统计"


class StatAttr:
    ITEM_NAME = "商品名称"
    SPEC_AMOUNT = "规格(数字)"
    SPEC_UNIT = "规格(单位)"
    SPEC = "规格"
    ADD_AMOUNT = "进库数量"
    PRICE = "单价"
    TOTAL_PRICE = "总价"
    NOTES = "备注"
    DATE = "操作日期"
    KG = "kg"
    G = "g"
    L = "l"
    ML = "ml"


input_item_attributes = [StatAttr.ITEM_NAME, StatAttr.SPEC_AMOUNT, StatAttr.SPEC_UNIT, StatAttr.ADD_AMOUNT, StatAttr.PRICE, StatAttr.NOTES]
display_item_attributes = [StatAttr.ITEM_NAME, StatAttr.ADD_AMOUNT, StatAttr.SPEC, StatAttr.PRICE, StatAttr.TOTAL_PRICE, StatAttr.NOTES, StatAttr.DATE]
units = [StatAttr.KG, StatAttr.G, StatAttr.L, StatAttr.ML]  # todo: 斤？
from web3 import Web3
from web3.contract import Contract

Peoples = ["王建国", "李红梅", "张明远", "刘芳", "陈志强", "杨丽华", "赵伟", "周静", "吴刚", "郑晓燕"]


def get_data(w3: Web3, contract: Contract) -> list:
    # 检查可用账户数量
    available_accounts = len(w3.eth.accounts)
    if available_accounts < 10:  # 至少需要10个账户
        raise Exception(f"需要至少10个账户，但只有{available_accounts}个可用账户")
    
    Ids = []
    Ids.append(get_supplier(w3, contract))
    Ids.append(get_producer(w3, contract))
    Ids.append(get_wholesaler(w3, contract))
    Ids.append(get_retailer(w3, contract))
    return Ids


def check_object_exists(w3: Web3, contract: Contract, account_index: int) -> bool:
    try:
        obj = contract.functions.getObject(w3.eth.accounts[account_index]).call()
        return bool(obj[0])  # 如果名称不为空，说明对象已存在
    except Exception:
        return False


def get_supplier(w3: Web3, contract: Contract):
    ids = []
    # 供应商 1 - 贵州茅台酒原料基地
    if not check_object_exists(w3, contract, 0):
        tx_hash1 = contract.functions.createObject(
            "贵州茅台酒原料基地",  # 名称
            "0851-12345678",  # 电话号码
            "https://pic.vjshi.com/2022-10-16/1c6eb7586c7a46bdbc36172876dbd1e9/00001.jpg?x-oss-process=style/watermark", 
            "原料供给",  # 类别
            "贵州省仁怀市茅台镇赤水河畔",  # 地址
            "茅台酒专用高粱种植基地，采用传统种植方式，确保原料品质",  # 描述
        ).transact({"from": w3.eth.accounts[0]})
        w3.eth.wait_for_transaction_receipt(tx_hash1)
    ids.append(0)

    # 供应商 2 - 茅台镇水源保护基地
    if not check_object_exists(w3, contract, 1):
        tx_hash2 = contract.functions.createObject(
            "茅台镇水源保护基地",  # 名称
            "0851-87654321",  # 电话号码
            "https://x0.ifengimg.com/ucms/2023_20/DF19F04B7971B97D4C3EE918579291ECF1D62A54_size1802_w1600_h900.jpg",
            "原料供给",  # 类别
            "贵州省仁怀市茅台镇赤水河上游",  # 地址
            "茅台酒专用水源保护基地，确保水质纯净",  # 描述
        ).transact({"from": w3.eth.accounts[1]})
        w3.eth.wait_for_transaction_receipt(tx_hash2)
    ids.append(1)

    return ids


def get_producer(w3: Web3, contract: Contract):
    ids = []
    # 生产商 1 - 茅台酒厂第一车间
    if not check_object_exists(w3, contract, 2):
        tx_hash3 = contract.functions.createObject(
            "茅台酒厂第一车间",  # 名称
            "0851-23456789",  # 电话号码
            "https://pic.huitu.com/res/20221025/1417944_20221025204453674217_1.jpg",
            "产品生产",  # 类别
            "贵州省仁怀市茅台镇茅台酒厂",  # 地址
            "茅台酒核心生产车间，采用传统工艺酿造",  # 描述
        ).transact({"from": w3.eth.accounts[2]})
        w3.eth.wait_for_transaction_receipt(tx_hash3)
    ids.append(2)

    # 生产商 2 - 茅台酒厂第二车间
    if not check_object_exists(w3, contract, 3):
        tx_hash4 = contract.functions.createObject(
            "茅台酒厂第二车间",  # 名称
            "0851-34567890",  # 电话号码
            "https://n.sinaimg.cn/sinakd202149s/88/w1080h608/20210409/d500-knipfsf6093546.jpg",
            "产品生产",  # 类别
            "贵州省仁怀市茅台镇茅台酒厂",  # 地址
            "茅台酒现代化生产车间，确保产品品质",  # 描述
        ).transact({"from": w3.eth.accounts[3]})
        w3.eth.wait_for_transaction_receipt(tx_hash4)
    ids.append(3)

    return ids


def get_wholesaler(w3: Web3, contract: Contract):
    ids = []
    # 批发商 1 - 贵州茅台酒销售有限公司
    if not check_object_exists(w3, contract, 4):
        tx_hash6 = contract.functions.createObject(
            "贵州茅台酒销售有限公司",  # 名称
            "0851-56789012",  # 电话号码
            "https://pic1.zhimg.com/v2-4c9bbb805ee7992ac199e6ed475b4f1c_r.jpg",
            "批发销售",  # 类别
            "贵州省贵阳市观山湖区茅台大厦",  # 地址
            "茅台酒官方授权批发商，负责全国市场供应",  # 描述
        ).transact({"from": w3.eth.accounts[4]})
        w3.eth.wait_for_transaction_receipt(tx_hash6)
    ids.append(4)

    # 批发商 2 - 茅台酒区域总代理
    if not check_object_exists(w3, contract, 5):
        tx_hash7 = contract.functions.createObject(
            "茅台酒区域总代理",  # 名称
            "0851-67890123",  # 电话号码
            "https://e0.ifengimg.com/08/2019/0629/43AA59F6EDB4CC52A4BC601BB3ECDF5159F6F253_size64_w640_h423.jpeg",
            "批发销售",  # 类别
            "贵州省贵阳市南明区茅台路88号",  # 地址
            "茅台酒区域总代理，负责区域市场供应",  # 描述
        ).transact({"from": w3.eth.accounts[5]})
        w3.eth.wait_for_transaction_receipt(tx_hash7)
    ids.append(5)

    return ids


def get_retailer(w3: Web3, contract: Contract):
    ids = []
    # 零售商 1 - 茅台酒官方旗舰店
    if not check_object_exists(w3, contract, 6):
        tx_hash1 = contract.functions.createObject(
            "茅台酒官方旗舰店",  # 名称
            "0851-78901234",  # 电话号码
            "https://xqimg.imedao.com/17a576cde124b5eb3fe18a9c.png!800.jpg",
            "零售销售",  # 类别
            "贵州省贵阳市云岩区中华北路1号",  # 地址
            "茅台酒官方直营店，提供正品保证",  # 描述
        ).transact({"from": w3.eth.accounts[6]})
        w3.eth.wait_for_transaction_receipt(tx_hash1)
    ids.append(6)

    # 零售商 2 - 茅台酒专卖店
    if not check_object_exists(w3, contract, 7):
        tx_hash2 = contract.functions.createObject(
            "茅台酒专卖店",  # 名称
            "0851-89012345",  # 电话号码
            "https://x0.ifengimg.com/ucms/2022_50/3D92CE2001E722B5EBF57CEEC3316202E55788DF_size280_w1620_h1080.jpg",
            "零售销售",  # 类别
            "贵州省贵阳市南明区遵义路2号",  # 地址
            "茅台酒授权专卖店，提供专业服务",  # 描述
        ).transact({"from": w3.eth.accounts[7]})
        w3.eth.wait_for_transaction_receipt(tx_hash2)
    ids.append(7)

    # 零售商 3 - 茅台酒体验店
    if not check_object_exists(w3, contract, 8):
        tx_hash3 = contract.functions.createObject(
            "茅台酒体验店",  # 名称
            "0851-90123456",  # 电话号码
            "https://n.sinaimg.cn/sinakd20211007s/580/w832h548/20211007/eb92-de1209f78cc137a25fbe8ce55633cce3.jpg",
            "零售销售",  # 类别
            "贵州省贵阳市观山湖区金阳大道3号",  # 地址
            "茅台酒体验店，提供品鉴服务",  # 描述
        ).transact({"from": w3.eth.accounts[8]})
        w3.eth.wait_for_transaction_receipt(tx_hash3)
    ids.append(8)

    # 零售商 4 - 茅台酒文化馆
    if not check_object_exists(w3, contract, 9):
        tx_hash4 = contract.functions.createObject(
            "茅台酒文化馆",  # 名称
            "0851-01234567",  # 电话号码
            "https://umeet.moutai.com.cn/gzmtstnycyfzyxgs/xwzx95/jtxw9/573090/file0002.png",
            "零售销售",  # 类别
            "贵州省贵阳市花溪区青岩古镇",  # 地址
            "茅台酒文化展示与销售中心",  # 描述
        ).transact({"from": w3.eth.accounts[9]})
        w3.eth.wait_for_transaction_receipt(tx_hash4)
    ids.append(9)

    return ids
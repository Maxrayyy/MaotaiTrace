from flask import Flask, jsonify, request
from web3 import Web3, HTTPProvider
import json
from data import get_data, Peoples
import os
import random
import uuid
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# 连接本地 Ganache
ganache_url = "http://127.0.0.1:7545"
w3 = Web3(HTTPProvider(ganache_url))

# 确保我们已经连接到以太坊节点
assert w3.is_connected()

# 载入 ABI 和合约地址
with open("MaotaiTrace_abi.json", "r", encoding="utf-8") as abi_definition:
    abi = json.load(abi_definition)

# 使用默认合约地址，如果没有设置环境变量
default_contract_address = "0xe5865acb3c95df20595adae99f4f55807f964e63"
contract_address = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS", default_contract_address))
contract = w3.eth.contract(address=contract_address, abi=abi)

# 获取节点数据
ids_list = get_data(w3, contract)

START_TIME = datetime(2000, 1, 1)
END_TIME = datetime(2020, 12, 31)

def generate_random_datatime(start_date, time_between_dates: timedelta):
    random_number_of_days = random.randrange(time_between_dates.days)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date

def datetime_to_timestamp_string(dt: datetime):
    timestamp = time.mktime(dt.timetuple())
    return str(int(timestamp))

def new_product():
    # 随机原料提供
    _id = str(uuid.uuid4())
    date_time = generate_random_datatime(START_TIME, END_TIME - START_TIME)
    
    # 随机选择原料供应商
    supplier_ids = ids_list[0]
    supplier_id = random.choice(supplier_ids)
    tx_hash0 = contract.functions.createProduct(
        _id,
        datetime_to_timestamp_string(date_time),
        w3.eth.accounts[supplier_id],
        Peoples[random.randint(0, len(Peoples) - 1)],
    ).transact({"from": w3.eth.accounts[supplier_id]})
    w3.eth.wait_for_transaction_receipt(tx_hash0)

    # 随机产品生产
    date_time = generate_random_datatime(date_time, END_TIME - date_time)
    producer_ids = ids_list[1]
    producer_id = random.choice(producer_ids)
    tx_hash1 = contract.functions.transferProduct(
        _id,
        datetime_to_timestamp_string(date_time),
        w3.eth.accounts[producer_id],
        Peoples[random.randint(0, len(Peoples) - 1)],
    ).transact({"from": w3.eth.accounts[supplier_id]})
    w3.eth.wait_for_transaction_receipt(tx_hash1)

    # 随机产品批发
    date_time = generate_random_datatime(date_time, END_TIME - date_time)
    wholesaler_ids = ids_list[2]
    wholesaler_id = random.choice(wholesaler_ids)
    tx_hash2 = contract.functions.transferProduct(
        _id,
        datetime_to_timestamp_string(date_time),
        w3.eth.accounts[wholesaler_id],
        Peoples[random.randint(0, len(Peoples) - 1)],
    ).transact({"from": w3.eth.accounts[producer_id]})
    w3.eth.wait_for_transaction_receipt(tx_hash2)

    # 随机是否零售（70%概率）
    if random.random() < 0.7:
        date_time = generate_random_datatime(date_time, END_TIME - date_time)
        retailer_ids = ids_list[3]
        retailer_id = random.choice(retailer_ids)
        tx_hash3 = contract.functions.transferProduct(
            _id,
            datetime_to_timestamp_string(date_time),
            w3.eth.accounts[retailer_id],
            Peoples[random.randint(0, len(Peoples) - 1)],
        ).transact({"from": w3.eth.accounts[wholesaler_id]})
        w3.eth.wait_for_transaction_receipt(tx_hash3)

    return _id

def get_product(_id):
    product_info = contract.functions.getProduct(_id).call()
    return product_info

def get_object(address):
    object_info = contract.functions.getObject(address).call()
    return object_info

# 初始化数据（可选）
@app.route('/init', methods=['POST'])
def init_data():
    try:
        ids = get_data(w3, contract)
        return jsonify({"status": "success", "data": ids})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取所有对象信息
@app.route('/objects', methods=['GET'])
def get_all_objects():
    try:
        # 获取所有账户
        accounts = w3.eth.accounts
        result = []
        
        # 遍历所有账户，检查是否有对象信息
        for account in accounts:
            try:
                obj = contract.functions.getObject(account).call()
                # 检查对象是否有有效信息（至少名称不为空）
                if obj[0]:  # 如果名称不为空
                    result.append({
                        "address": account,
                        "name": obj[0],
                        "phone": obj[1],
                        "image": obj[2],
                        "category": obj[3],
                        "address": obj[4],
                        "description": obj[5],
                    })
            except Exception:
                continue  # 如果获取对象信息失败，跳过该账户
                
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 创建新产品
@app.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.json
        product_id = data.get('id')
        date_time = data.get('dateTime')
        passed_object = data.get('passedObject')
        verifier = data.get('verifier')
        
        tx_hash = contract.functions.createProduct(
            product_id,
            date_time,
            Web3.to_checksum_address(passed_object),
            verifier
        ).transact({"from": w3.eth.accounts[0]})
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({
            "status": "success",
            "transaction_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 获取产品信息
@app.route('/products/<product_id>', methods=['GET'])
def get_product_info(product_id):
    try:
        product_info = get_product(product_id)
        result = []
        for info in product_info:
            result.append({
                "dateTime": info[0],
                "passedObject": info[1],
                "verifier": info[2]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 转移产品
@app.route('/products/transfer', methods=['POST'])
def transfer_product():
    try:
        data = request.json
        product_id = data.get('id')
        from_address = data.get('from')
        to_address = data.get('to')
        
        tx_hash = contract.functions.transferProduct(
            product_id,
            Web3.to_checksum_address(from_address),
            Web3.to_checksum_address(to_address)
        ).transact({"from": w3.eth.accounts[0]})
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({
            "status": "success",
            "transaction_hash": receipt.transactionHash.hex()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title 茅台酒溯源智能合约
/// @notice 用于登记生产单位信息、酒品信息、追踪流转过程

contract Traceability {

    // 产品流转记录结构体
    struct ProductInfo {
        string dateTime;        // 流转时间
        address passedObject;   // 当前持有该产品的地址（对象）
        string verifier;        // 验证/检查者，例如质检人员
    }

    // 企业/对象信息结构体
    struct ObjectInfo {
        string name;             // 名称，例如“贵州茅台股份有限公司”
        string phoneNumber;      // 联系电话
        string website;          // 官网
        string category;         // 类别，例如“生产商”、“经销商”、“门店”
        string objectAddress;    // 地址（字符串格式，非钱包地址）
        string description;      // 描述信息，例如主营业务
    }

    // 所有注册对象的映射，使用地址作为唯一标识
    mapping(address => ObjectInfo) public Objects;

    // 产品 ID（如“MT20240521001”）映射到产品流转记录数组
    mapping(string => ProductInfo[]) public products;

    // ========== 事件，用于前端监听 ==========
    event ObjectRegistered(address indexed registrant, string name); // 注册对象事件
    event ProductCreated(string indexed productId, address creator); // 创建产品事件
    event ProductTransferred(string indexed productId, address from, address to); // 产品转移事件

    /// @notice 注册对象（如生产商、经销商）
    function createObject(
        string memory _name,
        string memory _phoneNumber,
        string memory _website,
        string memory _category,
        string memory _objectAddress,
        string memory _description
    ) public {
        require(bytes(Objects[msg.sender].name).length == 0, "Object already exists");
        Objects[msg.sender] = ObjectInfo(_name, _phoneNumber, _website, _category, _objectAddress, _description);
        emit ObjectRegistered(msg.sender, _name);
    }

    /// @notice 创建新产品（通常是生产厂商调用）
    /// @param _id 产品唯一编号（如“MT20240521001”）
    /// @param _dateTime 创建时间
    /// @param _passedObject 初始持有者地址（应为msg.sender）
    /// @param _verifier 质检或创建时的验证信息
    function createProduct(
        string memory _id,
        string memory _dateTime,
        address _passedObject,
        string memory _verifier
    ) public {
        require(products[_id].length == 0, "Product ID already exists");
        require(msg.sender == _passedObject, "Only the initial owner can register product");

        products[_id].push(ProductInfo(_dateTime, _passedObject, _verifier));
        emit ProductCreated(_id, _passedObject);
    }

    /// @notice 转移产品所有权（必须由当前持有人发起）
    function transferProduct(
        string memory _id,
        string memory _dateTime,
        address _passedObject,
        string memory _verifier
    ) public {
        require(products[_id].length > 0, "Product does not exist");

        ProductInfo memory last = products[_id][products[_id].length - 1];
        require(msg.sender == last.passedObject, "Only current owner can transfer product");

        products[_id].push(ProductInfo(_dateTime, _passedObject, _verifier));
        emit ProductTransferred(_id, msg.sender, _passedObject);
    }

    /// @notice 获取某产品的全部流转记录
    function getProduct(string memory _id) public view returns (ProductInfo[] memory) {
        return products[_id];
    }

    /// @notice 获取指定地址的对象信息
    function getObject(address _address) public view returns (
        string memory, string memory, string memory,
        string memory, string memory, string memory
    ) {
        require(bytes(Objects[_address].name).length > 0, "Object does not exist");
        ObjectInfo memory obj = Objects[_address];
        return (
            obj.name,
            obj.phoneNumber,
            obj.website,
            obj.category,
            obj.objectAddress,
            obj.description
        );
    }
}

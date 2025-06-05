# 茅台酒区块链溯源系统

基于区块链技术的茅台酒产品溯源系统，实现从原料供应、生产、批发到零售的全流程可追溯。

## 环境要求

- Python 3.8+
- Node.js 14+
- Ganache (GUI版本)
- Remix IDE
- MetaMask 浏览器插件

## 安装步骤

### 1. 安装 Python 依赖
```bash
pip install flask web3 gradio
```

### 2. 安装 Ganache
1. 访问 [Ganache 官网](https://trufflesuite.com/ganache/) 下载 GUI 版本
2. 安装并运行 Ganache
3. 创建新的工作区（Workspace）
4. 确保 RPC Server 运行在 `http://127.0.0.1:7545`

### 3. 部署智能合约
1. 访问 [Remix IDE](https://remix.ethereum.org/)
2. 创建新文件 `MaotaiTrace.sol`，复制合约代码
3. 编译合约（确保编译器版本与合约兼容）
4. 在部署页面：
   - 环境选择 "Injected Provider - MetaMask"
   - 确保 MetaMask 连接到 Ganache 网络
   - 点击 "Deploy" 部署合约
5. 部署成功后，复制合约地址
6. 将合约地址更新到 `backend.py` 中的 `default_contract_address` 变量

### 4. 配置 MetaMask
1. 安装 MetaMask 浏览器插件
2. 添加 Ganache 网络：
   - 网络名称：使用默认名称
   - RPC URL：http://127.0.0.1:7545
   - 链 ID：1337
   - 货币符号：ETH
3. 导入 Ganache 提供的测试账户（私钥）

## 运行项目

### 1. 启动后端服务
```bash
python backend.py
```
后端服务将在 http://127.0.0.1:5000 运行

### 2. 启动前端服务
```bash
python frontend.py
```
前端界面将在 http://127.0.0.1:7860 运行

## 使用说明

### 生成产品
1. 在"茅台酒产品溯源链"标签页
2. 点击"随机生成产品"按钮
3. 系统会自动生成一个完整的溯源链

### 查询溯源信息
1. 在"溯源信息查询"标签页
2. 输入要查询的地址
3. 点击"查询溯源信息"按钮
4. 查看完整的溯源信息

## 重置数据

如果需要重置区块链数据：
1. 在 Ganache GUI 中点击"重置"按钮
2. 重新部署智能合约
3. 更新 `backend.py` 中的合约地址
4. 重启后端和前端服务
5. 重新初始化数据

## 项目结构

```
maotai_blockchain_demo/
├── backend.py          # 后端服务
├── frontend.py         # 前端界面
├── data.py            # 数据生成模块
├── MaotaiTrace.sol    # 智能合约
├── MaotaiTrace_abi.json # 合约 ABI
└── README.md          # 项目说明
```

## 注意事项

1. 确保 Ganache 在运行状态
2. 确保 MetaMask 已连接到 Ganache 网络
3. 合约地址变更后需要更新 `backend.py`
4. 重置区块链后需要重新部署合约

## 常见问题

1. **连接失败**
   - 检查 Ganache 是否运行
   - 确认 RPC URL 是否正确
   - 验证 MetaMask 网络配置

2. **合约部署失败**
   - 检查 Remix IDE 编译器版本
   - 确认 MetaMask 账户余额充足
   - 验证合约代码是否有误

3. **图片显示异常**
   - 检查图片 URL 是否可访问
   - 确认网络连接正常
   - 尝试重置区块链数据

# Model Info Object

模型信息，可以用于访问模型
以下是结构示例：

``` json
{
  "name": "Model Name", // 可读的模型名称
  "base_url": "https://api.example.com", // 模型 API 的 URL
  "endpoint": "/v1",
  "fetch_models_endpoint": "/models", // 获取模型列表的 API 端点
  "id": "model-id", // 面向厂商的模型 ID
  "uid": "deepseek/model-id", // 模型的唯一标识符，可用于查询
  "parent": "Deepseek", // 该模型所属的模型组
  "parent_id": "deepseek", // 模型组 ID，可用于查询
  "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", // API 密钥
  "limit": { // 限制，包含以下字段
    "max_connections": 100, // 最大连接数
    "max_keepalive_connections": 20, // 最大保持连接数
    "keepalive_expiry": 5, // 保持连接的过期时间，单位为秒
  },
  "timeout": { // 超时时间，单位为秒，也可以填写一个数字，表示总超时
    "connect": 10, // 连接超时
    "read": 30, // 读取超时
    "write": 30, // 写入超时
    "pool": 30 // 连接池超时
  }
}
```
# API Info

该文件作为索引，用于指导模型信息获取与存储。

```json
{
  // 一个固定的字符串，用于标识配置文件类型
  "type": "model_group_config.v1",

  // 模型组列表
  "providers": [
    {
      // 模型组名称
      "name": "OpenAI API Group",

      // 模型组 ID，用于查询与唯一标识
      "id": "openai",

      // 模型API密钥环境变量的名称
      // 此处的这种格式也可以写为
      // "api_key_env": "OPENAI_API_KEY"
      // 表示只有一项且该项权重为 100%
      "api_key_env": {

        // 键为环境变量名称，值为权重
        "OPENAI_API_KEY": 1 
      },

      // API 的基础 URL
      "base_url": "https://api.openai.com",

      // API 的基础路径
      "endpoint": "/v1",
      
      // 获取模型列表的 API 路径
      "fetch_models_endpoint": "/models",

      // 连接限制，包含以下字段
      "limit": {

        // 最大连接数
        "max_connections": 100,

        // 最大保持连接数
        "max_keepalive_connections": 20,

        // 保持连接的过期时间，单位为秒
        "keepalive_expiry": 5,
      },

      // 超时时间，单位为秒，这里也可以填写一个数字，表示总超时
      "timeout": {

        // 连接超时
        "connect": 10,

        // 读取超时
        "read": 30,

        // 写入超时
        "write": 30,

        // 连接池超时
        "pool": 30
      },
      
      // 模型手动填充列表，目前为保留字段
      "models": [],
      
      // HTTP 代理
      "proxy": null,
    }
  ],
  
  // 模型库文件，如果不写则每次都直接从供应商获取模型信息
  "library_file": "providers_library.json",
}
```
# Model Info Server APIs

通过 API 获取模型信息

- [Get Model](./get_model.md)
- [Get All Models](./get_all_models.md)
- [Get API Key](./get_api_key.md)
- [Alived](./alived.md)
- [*\*Exception Response*](./exception_response.md)

PS: 除了 Alived API
所有 API 都需要使用 API Key 进行认证
验证方法为 Bearer 认证
例如: `Authorization: Bearer <API_KEY>`
具体 API Key 由环境变量 `API_KEY` 定义
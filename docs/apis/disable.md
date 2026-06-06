# Disable Model

禁用指定模型

- `/disable/{model_id}`
  - **method**: `POST`
  - **params**:
    - `model_id`: 模型 UID
  - **response**:
    - `timeout`: 超时时间，单位 `ns`
  - **response**:
    - `message`: 响应信息
    - `success`: 成功禁用的模型数量
    - `total`: 实际匹配到的模型数量
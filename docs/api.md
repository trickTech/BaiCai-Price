# 接口文档
## 总述
### 接口格式
所有接口均以`api`开头，后跟实体名与相应参数，无特殊说明，请求方法均为get。

如:

    api/vegetable/1

## 附加参数
### 分页

分页使用url参数,key为`page`

    api/vegetable/1?page=1

### 排序

排序使用url参数,key为`order_by`,后跟attribute名

    api/record/today?order_by=avg_price

attribute不存在则不排序

是否翻转顺序，key为`reversed`,值为`true`(不区分大小写)

    api/record/today?order_by=avg_price&reversed=true


## 接口
### record/today
#### 描述：

获取当天的蔬菜记录
    
#### 返回值：
    
    {
    "element_per_page": 15,
    "total_page": 26,
    "content": [
    {
    "recorded_at": "2016-10-14",
    "id": 19,
    "item_name": "油菜",
    "avg_price": 114,
    "lowest_price": 100,
    "highest_price": 130
    },]
    }
	
### vegetable/veg_id
#### 描述
获取某种蔬菜的的所有记录

#### 返回值

    {
    "element_per_page": 15,
    "total_page": 1,
    "content": [
    {
    "recorded_at": "2016-10-13",
    "id": 1,
    "item_name": "大白菜",
    "avg_price": 45,
    "lowest_price": 30,
    "highest_price": 60
    },
    {
    "recorded_at": "2016-10-14",
    "id": 1,
    "item_name": "大白菜",
    "avg_price": 43,
    "lowest_price": 35,
    "highest_price": 50
    }
    ]
    }

### vegetable/search (POST)
#### 描述
搜索蔬菜并返回最新的记录

#### 参数
    'item_name' : '物品名'

#### 返回值
    {'content': [{'avg_price': 105,
       'created_at': '2016-10-04',
       'highest_price': 130,
       'id': 17,
       'lowest_price': 80,
       'veg_name': '菜花'},
      {'avg_price': 130,
       'created_at': '2016-10-04',
       'highest_price': 180,
       'id': 18,
       'lowest_price': 80,
       'veg_name': '绿菜花'},
      {'avg_price': 165,
       'created_at': '2016-10-04',
       'highest_price': 180,
       'id': 79,
       'lowest_price': 150,
       'veg_name': '黄心菜'}],
     'element_per_page': 15,
     'total_page': 2}

### record/history/date
#### 描述
获取某日的所有记录
#### 参数
date : %Y-%m-%d: 2015-4-22
#### 返回值
    
    {
    "element_per_page": 15,
    "total_page": 26,
    "content": [
    {
    "highest_price": 130,
    "avg_price": 114,
    "lowest_price": 100,
    "id": 19,
    "item_name": "油菜",
    "recorded_at": "2016-10-14"
    },]
    }


# 接口文档
## 总述
### 接口格式
所有接口均以`api`开头，后跟实体名与相应参数，无特殊说明，请求方法均为get。

如:

    api/vegetable/1

分页使用url参数,key为`page`

    api/vegetable/1?page=1
    
## 接口
### record/today
#### 描述：

获取当天的蔬菜记录
    
#### 返回值：

    [
    	{"lowest_price": 350,
    	 "created_at": "2016-10-01",
    	 "veg_name": "\u849c\u82d7",
    	 "avg_price": 445,
    	 "highest_price": 540}
	]
	
### vegetable/veg_id
#### 描述
获取某种蔬菜的的所有记录

#### 返回值

	[
		{
			"lowest_price": 350,
			"created_at": "2016-10-01",
			"veg_name": "\u849c\u82d7",
			"avg_price": 445,
			"highest_price": 540
		}
	]


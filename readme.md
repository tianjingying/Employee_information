#menu
##1.Employee_information[介绍]
>本程序实现员工信息表的增，删，改，查操作

##2.need environment[环境需求]
`Python版本 >= Python3.0`

##3.move[移植问题]
    暂时不存在移植问题

##4.menu.py 1.0 feature[特性]
>*添加员工记录，以phone做唯一键，staff_id自增
>*可进行模糊查询 ， 例如：
  select name,age from staff_table where age > 22
  select  * from staff_table where age > 22 and dept = it
  select  * from staff_table where age >= 22 and dept like it

  等等

>*可修改记录，仅支持sql 语句修改方式
>*可根据输入的员工id 号删除员工记录

##5.important .py[重要的Python文件]
>*	Employee.py
>*	staff_table.csv

##6.how to[怎么执行]
>* python3 Employee.py ， 运行程序后按照界面的提示操作

##7.参见本目录中的 "flowsheet.jpg"文件

##8.博客地址：
	http://5506100.blog.51cto.com/
	
	
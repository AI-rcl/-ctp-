#基于事件驱动的ctp交易程序示例

1、行情订阅演示效果如下（qt页面模仿vnpy的页面来实现），输入要订阅的合约，回车即能看到行情

2、其他下单，撤单、持仓明细、策略等功能都大致是这个思路，用事件引擎注册相应的函数，再在qt中关联相应的ui控件。

![alt text](1716178048823.png)
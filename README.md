# hydrometer_esp32_micropython
A digital wireless hydrometer inspired by Tilt & iSpindel.  Powered by Micropython ESP32.

### Features
- [X] 2种运行模式，校准模式 & 工作模式，由拨动试开关控制。Pin IN加下拉电阻，低电平时为工作模式，高电平时为校准模式。
- [X] 校准模式下，点亮一个LED灯珠以示区别。
- [X] 校准模式：开启AP和STA，启动http服务器，提供校准和设置页面。
- [X] 校准采用二次多项式回归y = a\*x\*x + b\*x + c，其中x为倾角角度，y为比重数值。可选择倾角对应的比重单位（sg vs. p），建议使用p，以提高肉眼读取精度。
- [X] 校准数据保存在ESP32上，格式为json，内容如下。
```
{
  "unit": "p",
  "a": 0.016695786886914407,
  "b": -1.7010962658032376,
  "c": 0.016695786886914407
}
```
- [X] 校准模式下，ESP32每5秒读取一次倾角角度。
- [X] 校准模式下，设置选项包括：设置比重计自己的AP名称，设置连接发酵箱的Wifi信号，设置连接路由器wifi型号，设置工作模式下的唤醒（采样）频率（默认每20分钟1次）。
- [X] 工作模式：开启STA，仅提供http client服务，根据唤醒频率设置自动唤醒向发酵箱发送：SG比重数据（发送给发酵箱的比重数据统一为SG），电量百分比，格式如下。
```
{
  "sg": 1.057,
  "battery": 60
}
```
- [X] 工作模式下，数据发送到发酵箱后台，再由发酵箱前台读取。
```
{
  sg: 1.017,
  battery: 55,
}
// *注意：发酵箱显示的比重默认单位为sg，读取比重计数据时要先根据情况转换单位。
```
- [ ] 另外，比重数据需要记录，如下gravityDataList
```
chartDataSeries: {
  setTempDataList: [],
  chamberTempDataList: [],
  wortTempDataList: [],
  gravityDataList: [],
}
```

### 使用ecStat绘图，示例代码
```javascript
//ecStat 是 ECharts 的统计扩展，需要额外添加扩展脚本，参加上方“脚本”
// 详情请移步 https://github.com/ecomfe/echarts-stat
// 图中的曲线是通过多项式回归拟合出的

 var data = [
     [27.4, 1.0],
     [61.25, 1.074],
     [62.63, 1.077],
     [60.6, 1.071],
     [58.85, 1.067],
     [52, 1.048],
     [48.4, 1.039],
     [42.4, 1.027],
     [39, 1.020],
     [32, 1.008]
 ];

 var myRegression = ecStat.regression('polynomial', data, 2);
 
 console.log(myRegression.expression)
 console.log(myRegression.parameter)

 myRegression.points.sort(function(a, b) {
     return a[0] - b[0];
 });

 myChart.setOption({

     tooltip: {
         trigger: 'axis',
         axisPointer: {
             type: 'cross'
         }
     },
     title: {
         text: 'Tilt-Gravity Regression',
         left: 'center',
         top: 16
     },
     xAxis: {
         type: 'value',
         name: 'Tilt Angle',
         nameLocation: 'middle',
         nameGap: 30,
         min: 20,
         splitLine: {
             lineStyle: {
                 type: 'dashed'
             }
         },
         splitNumber: 20
     },
     yAxis: {
         type: 'value',
         name: 'Gravity',
         nameLocation: 'middle',
         nameGap: 40,
         min: 0.99,
         splitLine: {
             lineStyle: {
                 type: 'dashed'
             }
         },
         splitNumber: 10
     },
     series: [{
         name: 'scatter',
         type: 'scatter',
         label: {
             emphasis: {
                 show: true
             }
         },
         data: data
     }, {
         name: 'line',
         type: 'line',
         smooth: true,
         showSymbol: false,
         data: myRegression.points,
         markPoint: {
             itemStyle: {
                 normal: {
                     color: 'transparent'
                 }
             },
             label: {
                 normal: {
                     show: true,
                     position: 'left',
                     formatter: myRegression.expression,
                     textStyle: {
                         color: '#333',
                         fontSize: 14
                     }
                 }
             },
             data: [{
                 coord: myRegression.points[myRegression.points.length - 1]
             }]
         }
     }]
 });
```

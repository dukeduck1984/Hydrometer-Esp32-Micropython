# Hydrometer-Esp32-Micropython
A digital wireless hydrometer inspired by Tilt & iSpindel.  Powered by Micropython ESP32.


## Features
- Upon switching on, the battery level will be indicated by the LED color - green means the battery is healthy while red means the power may not be enough for the whole fermentation process.
- A reed switch is used to change mode, put a magnet close to the reed switch while the blue LED is flashing will boot the Hydrometer into calibration mode in which you can change the settings and calibrate the device.
- This hydrometer is self-contained which means you can do the calibration without for example a spread sheet.  The polynomial regression for the plato/sg tilt angle relationship is already built into the front-end.  So just follow the guide and you can do the calibration easily.  The calibration even has a temperature correction feature which is optional, so that the calibration is still valid even if your tap water is really cold or warm.
- The API is compatible with iSpindel, so it can be a drop-in replacement and is compatible with CraftBeerPi (also check out my Fermenter-ESP32, in fact a microcontroller is more suitable for this kind of stuff than a single board computer).
- Data can be optionally sent to either the fermentation controller or a MQTT broker (e.g. Ubidots).
- Same as the Tilt or the iSpindel, it has a DS18B20 temp sensor to measure 'the wort temp' which can be a reference for those brewers who don't have a temp sensor measuring the wort temp directly.

### 功能
- [X] 2种运行模式，校准模式 & 工作模式，由磁铁触发干簧管控制。Pin IN加上拉电阻，触发高电平时为校准模式，否则在1分钟后进入工作模式。
- [X] 电源开关采用水银开关，试管圆头向上摆放为断电，圆头向下则通电。
- [X] 校准模式下，点亮板载LED灯珠以示区别。
- [X] 在等待用户选择模式的1分钟里，板载LED闪烁，方便用户区分
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
- [X] 工作模式下，根据用户设置的数据发送去向，开启STA，连接发酵箱AP信号（数据发至发酵箱），或家中无线路由信号（数据发至MQTT服务器）
- [X] 工作模式下，根据唤醒频率设置自动唤醒发送比重数据和电量。
- [X] 发送到发酵箱后台的数据如下
```
{
  "currentGravity": 1.057,
  "batteryLevel": 60,
  "updateIntervalSec": 1200
}
// *注意：发酵箱显示的比重默认单位为sg，读取比重计数据时要先根据情况转换单位。
```
- [X] 发送至MQTT服务器的数据如下
```
{
  "sg": 1.057,
  "battery": 60
}
```
- [X] 另外，比重数据需要记录，如下gravityDataList (此任务由发酵箱的前端完成)
```
chartDataSeries: {
  setTempDataList: [],
  chamberTempDataList: [],
  wortTempDataList: [],
  gravityDataList: [],
}
```
- [ ] 比重计内增加一个DS18B20温度传感器，根据温度对比重做纠正
```
cg = corrected specific gravity
mg = measured specific gravity
tr = temperature at time of reading (F)
tc = calibration temperature of hydrometer (F)

cg = mg * ((1.00130346 - 0.000134722124 * tr + 0.00000204052596 * tr^2 - 0.00000000232820948 * tr^3) / (1.00130346 - 0.000134722124 * tc + 0.00000204052596 * tc^2 - 0.00000000232820948 * tc^3))
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

## API

### /connecttest
* GET
前台每2秒向后台请求，确认前后台之间的连接正常

### /calibration
* GET
读取比重计倾角数据，前台每10秒请求一次
```json5
{
  "tilt": 76.3
}
```

* POST
前台向后台传递拟合后的系数，并进行保存
```json5
{
  "unit": "p",
  "a": 0.016695786886914407,
  "b": -1.7010962658032376,
  "c": 0.016695786886914407
}
```

### /settings
* GET
向后台获取用户设置参数
```json5
{
  "deepSleepIntervalMs": 10000,
  "apSsid": "Hydrometer",
  "wifi": {
    "ssid": "",
    "pass": ""
  },
  "fermenterAp": {
    "enabled": true,
    "ssid": "Fermenter",
    "pass": ""
  },
  "mqtt": {
    "enabled": false,
    "brokerAddr": "things.ubidots.com",
    "brokerPort": 1883,
    "username": "BBA-DASKLFJELFEL5646566WW",
    "password": "",
    "topic": "/v1.6/devices/hydrometer"
  },
  "wifiList": [
    "28#301",
    "28#301_ASUS",
    "Fermenter",
    "ChinaNet1234",
    "ChinaNet4542",
    "UnionCom8876"
  ]
}
```

* POST
向后台发送用户设置参数并保存
```json5
{
  "deepSleepIntervalMs": 10000,
  "apSsid": "Hydrometer",
  "wifi": {
    "ssid": "",
    "pass": ""
  },
  "fermenterAp": {
    "enabled": true,
    "ssid": "Fermenter",
    "pass": ""
  },
  "mqtt": {
    "enabled": false,
    "brokerAddr": "things.ubidots.com",
    "brokerPort": 1883,
    "username": "BBA-DASKLFJELFEL5646566WW",
    "password": "",
    "topic": "/v1.6/devices/hydrometer"
  }
}
```

### /wifi
* GET
获取Wifi热点列表
```json5
{
  "wifiList": [
    "28#301",
    "28#301_ASUS",
    "Fermenter",
    "ChinaNet1234",
    "ChinaNet4542",
    "UnionCom8876"
  ]
}
```

* POST
连接指定Wifi热点
```json5
{
  "ssid": "ChinaNet4542",
  "pass": "12345678"
}
```

### /mqtttest
向MQTT服务器发送测试信息
* POST
```json5
{
"mqtt": {
    "enabled": true,
    "brokerAddr": "things.ubidots.com",
    "brokerPort": 1883,
    "username": "BBA-DASKLFJELFEL5646566WW",
    "password": "",
    "topic": "/v1.6/devices/hydrometer"
  }
}
```

### /reboot
* GET


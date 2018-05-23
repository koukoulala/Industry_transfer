# Industrial Transfer:产业转移可视分析系统
	>IndustrialTransfer
		>index.html：主页面，css、fonts、images、js文件夹及style.css均是用于这个页面，用到的技术的是BootStrap
		>Stacked-to-Grouped Bars：D3.js实现的一种统计分析图，主要功能是展示每个地区的三种产业之间的转移，可以在stacked bar和grouped bar之间切换，并可以切换不同数据
			>index.html：主页面
			>d3.v4.min.js：D3的库，用的是V4版，目前最新版是V5
			>data:csv=>从csv文件中读取数据，数据分为三列，分别是province（应该为industry）、value和year
		>China Map：d3实现的中国地图，主要功能是展示产业在地区之间的转移，转移的起点用黄色点表示，终点用小白点表示，变化都有动画，点击click会添加省份
			>index.html
			>d3.v4.min.js
			>map data:china.json，中国地图的数据

1、Stacked-to-Grouped Bars 
	要添加数据的话要和我用到的数据格式相同：数据的编码格式需要是utf-8，数值间的间隔用','，可以用notepad++转换

2、ChinaMap
	这个用到的数据我直接写在index.html里了，city_from是产业转移的起始城市，from_beijing/shanghai/guangdong都是产业转移的对象，这些数组都可以改，其他部分不要改。
	city_from数组里的城市目前只有北京，所以开始时只展示北京的产业转移情况，点击click会更新这个数组，所以会逐渐添加城市
	在绘制出黄点和白点后2秒，会有模拟产业转移的动画，其实就是一些小白点动态的从黄点出发沿着直线移动到终点。